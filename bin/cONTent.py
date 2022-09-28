import sys 
import content.interface as intrf

if __name__ == '__main__':
    args = intrf.arguments_parser()
    if args.sub_prog == 'extract':
        import content.extraction as xtrct
        xtrct.main(args)
    elif args.sub_prog == 'distrib':
        import content.distribution as dstrb
        dstrb.main(args.input, args.outdir, args.fraction, args.prefix)
    elif args.sub_prog == 'coverage':
        import content.coverage as cvrg
        cvrg.main(args)
    else:
        print(intrf.PROG_DESCRIPTION)
        sys.exit()

