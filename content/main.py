import sys
import content.interface as intrf

def main():
    args = intrf.arguments_parser()

    match args.sub_prog:
        case "extract":
            import content.extraction as xtrct
            xtrct.main(args)

        case "distrib":
            import content.distribution as dstrb
            dstrb.main(args.input, args.outdir, args.fraction, args.prefix)
        
        case "coverage":
            import content.coverage as cvrg
            cvrg.main(args)
        
        case other:
            print(intrf.PROG_DESCRIPTION)
            sys.exit()

if __name__ == "__main__":
    main()
