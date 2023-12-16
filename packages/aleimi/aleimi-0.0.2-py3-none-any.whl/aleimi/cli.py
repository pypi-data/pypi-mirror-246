#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from aleimi import confgen, boltzmann, extractor, __version__, utils, processed
import argparse, os, yaml

"""
Tengo que adicionar la parte de los comandos extras para pasarselos a exrtractor
para la creacion de los templates, probar con los argumentos que se pasan
si alguno esta mal entonces dlanzar un warning o algo por el estilo
Tengo que ver esto bien, me falta por implemnetar lo fde .gjf
Y lo de el analisis para al menos psi4 y orca
    """


def _aleimi_run():
    """CLI of ``aleimi``
    """
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        help="The path to the directory were the molecule(s) is(are)",
        dest='suppl',
        type=str)
    parser.add_argument(
        '-p', '--params',
        help="Parameters to run ALEIMI",
        default=None,
        dest='params',
        type=str)
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f"aleimi: {__version__}")

    args = parser.parse_args()

    suppl = args.suppl
    params = args.params
    if not os.path.exists(args.suppl):
        raise FileNotFoundError(f"{args.suppl} does not exist or is not accessible.")

    # Getting the default kwargs of all the functions.
    confgen_keywords = utils.get_default_kwargs(confgen.main)
    boltzmann_keywords = utils.get_default_kwargs(boltzmann.main)
    extractor_keywords = utils.get_default_kwargs(extractor.main)
    used_keywords = {**confgen_keywords, **boltzmann_keywords, **boltzmann_keywords}
    if args.params:
        if not os.path.exists(params):
            raise FileNotFoundError(f"{params} does not exist or is not accessible.")

        with open(args.params, 'r') as params:
            user_keywords =  yaml.safe_load(params)

        for key in confgen_keywords.keys():
            if key in user_keywords:
                try:
                    confgen_keywords[key] = type(confgen_keywords[key])(user_keywords[key])  # Here I  am taking the type of the variable
                except:
                    raise ValueError(f"{user_keywords[key]} must be a {type(confgen_keywords[key])}-like")

        for key in boltzmann_keywords.keys():
            if key in user_keywords:
                try:
                    boltzmann_keywords[key] = type(boltzmann_keywords[key])(user_keywords[key])  # Here I  am taking the type of the variable
                except:
                    raise ValueError(f"{user_keywords[key]} must be a {type(boltzmann_keywords[key])}-like")

        for key in extractor_keywords.keys():
            if key in user_keywords:
                try:
                    extractor_keywords[key] = type(extractor_keywords[key])(user_keywords[key])  # Here I  am taking the type of the variable
                except:
                    raise ValueError(f"{user_keywords[key]} must be a {type(extractor_keywords[key])}-like")

    # Save the config as a yaml file
    with open('outparams.yml', 'w') as f:
        yaml.dump(used_keywords, f)

    mol_names = confgen.main(suppl, **confgen_keywords)
    for mol_name in mol_names:
        print(mol_name)
        utils.mopac(f"{mol_name}.mop")
        boltzmann.main(f"{mol_name}.arc", **boltzmann_keywords)
        extractor.main(f"{mol_name}.arc", f"{mol_name}_boltzmann.csv", **boltzmann_keywords)


def _aleimi_processed():
    """CLI of ``processed``
    """
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawTextHelpFormatter)


    parser.add_argument('--no_sub_dirs',
                        help ='Should be True if :meth:`aleimi.extractor.main` was used with ``mkdir = True``, by default True',
                        nargs = "?",
                        dest = 'no_sub_dirs',
                        const = False,
                        default = True,
                        type=bool)
    parser.add_argument('-e, --engine',
                        help ="psi4, gaussian or orca. It depends on the engine defined on :meth:`aleimi.extractor.main` was used with ``engine`` keyword, by default 'psi4'",
                        dest = 'engine',
                        default = 'psi4',
                        type=str)

    parser.add_argument('--xyz_out',
                        help ='If True, it will write the xyz coordinates of the conformer with the lowest energy, by default False',
                        nargs = "?",
                        dest = 'xyz_out',
                        const = True,
                        default = False,
                        type=bool)

    args = parser.parse_args()

    processed.main(
        SubDirs=not args.no_sub_dirs,
        engine=args.engine,
        xyz_out=args.xyz_out
    )
if __name__ == '__main__':
    pass
