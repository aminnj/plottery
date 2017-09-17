import ROOT as r
import os
import plottery as ply

"""
0 to print out all possible options and their defaults
1 to show two overlaid 1D hists
2 to show three TGraph ROC curves 
3 to show a TH2D with smart bin labels...fancy
"""
which_tests = [0]
# which_tests = [1, 2, 3]
which_tests = [4]
# which_tests = [2]

for which_test in which_tests:

    if which_test == 0:

        ply.Options().usage()

    if which_test == 1:

        scalefact_all = 1000
        scalefact_mc = 7
        
        nbins = 30
        h1 = r.TH1F("h1","h1",nbins,0,5)
        h1.FillRandom("gaus",int(scalefact_mc*6*scalefact_all))
        h1.Scale(1./scalefact_mc)

        h2 = r.TH1F("h2","h2",nbins,0,5)
        h2.FillRandom("expo",int(scalefact_mc*5.2*scalefact_all))
        h2.Scale(1./scalefact_mc)

        h3 = r.TH1F("h3","h3",nbins,0,5)
        h3.FillRandom("landau",int(scalefact_mc*8*scalefact_all))
        h3.Scale(1./scalefact_mc)

        hdata = r.TH1F("hdata","hdata",nbins,0,5)
        hdata.FillRandom("gaus",int(6*scalefact_all))
        hdata.FillRandom("expo",int(5.2*scalefact_all))
        hdata.FillRandom("landau",int(8*scalefact_all))

        ply.plot_hist(
                data=hdata,
                bgs=[h1,h2,h3],
                colors = [r.kRed-2, r.kAzure+2, r.kGreen-2],
                legend_labels = ["first", "second", "third"],
                options = {
                    "do_stack": True,
                    "legend_alignment": "bottom left",
                    # "legend_scalex": 1.3,
                    # "legend_scaley": 0.7,
                    # "legend_ncolumns": 2,
                    "legend_opacity": 0.5,
                    "extra_text": ["#slash{E}_{T} > 50 GeV","N_{jets} #geq 2","H_{T} > 300 GeV"],
                    "extra_text_xpos": 0.35,
                    # "yaxis_log": True,
                    "yaxis_moreloglabels": True,
                    "ratio_range":[0.8,1.2],
                    # "ratio_numden_indices": [0,1],
                    # "hist_disable_xerrors": True,
                    # "ratio_chi2prob": True,
                    "output_name": "test1.pdf",
                    "legend_percentageinbox": True,
                    "cms_label": "Preliminary",
                    "lumi_value": 1.,
                    "output_ic": True,
                    "us_flag": True,
                    # "output_jsroot": True,
                    }
                )


    elif which_test == 2:

        ply.plot_graph(
                [
                    # pairs of x coord and y coord lists --> normal line
                    ([0.1,0.2,0.3,0.4,0.5,0.6,0.7,1.0], [0.1,0.5,0.9,1.0,1.0,1.0,1.0,1.0]),
                    # pairs of x coord and y coord lists --> normal line
                    ([0.2,0.3,0.4,0.5,0.6,0.7,1.0], [0.3,0.5,0.7,0.8,0.9,0.95,1.0]),
                    # quadruplet of x, y, ydown,yup --> error band
                    ([0.1,0.2,0.3,0.4,0.5,0.6,0.7,1.0], [0.1,0.2,0.3,0.45,0.6,0.7,0.8,1.0],[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1],[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]),
                    ],
                colors = [r.kRed-2, r.kGreen-2, r.kAzure+2],
                legend_labels = ["red", "green", "blue"],
                options = {
                    "legend_alignment": "bottom right",
                    "legend_scalex": 0.7,
                    "xaxis_label": "bkg. eff.",
                    "yaxis_label": "sig. eff.",
                    "yaxis_log": True,
                    "yaxis_moreloglabels": True,
                    "yaxis_noexponents": True,
                    "xaxis_range": [0.1,1.0],
                    "yaxis_range": [0.1,1.0],
                    "title": "Crappy ROC curve",
                    "output_name": "test2.pdf",
                    "output_ic": True,
                    }
                )

        
    elif which_test == 3:

        xyg = r.TF2("xygaus","xygaus",0,10,0,10);
        xyg.SetParameters(1,5,2,5,2)  # amplitude, meanx,sigmax,meany,sigmay
        h2 = r.TH2F("h2","h2",10,0,10, 10,0,10)
        h2.FillRandom("xygaus",10000)
        ply.plot_hist_2d(
                h2,
                options = {
                    "zaxis_log": True,
                    "output_name": "test.pdf",
                    "bin_text_smart": True,
                    "output_name": "test3.pdf",
                    "us_flag": True,
                    # "us_flag_coordinates": [0.9,0.96,0.06],
                    "output_ic": True,
                    }
                )


    elif which_test == 4:

        ########################################
        ################# WIP ##################
        ########################################

        xyg = r.TF2("xygaus","xygaus",0,10,0,10);
        xyg.SetParameters(1,4,2,6,2)  # amplitude, meanx,sigmax,meany,sigmay
        h2 = r.TH2F("h2","h2",10,0,10, 10,0,10)
        h2.FillRandom("xygaus",10000)
        ply.plot_hist_2d_projections(
                h2,
                options = {
                    "zaxis_log": True,
                    "output_name": "test.pdf",
                    "bin_text_smart": False,
                    "output_name": "test4.pdf",
                    "us_flag": False,
                    # "us_flag_coordinates": [0.9,0.96,0.06],
                    "output_ic": True,
                    }
                )


