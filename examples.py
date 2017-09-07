import ROOT as r
import os
import plottery as ply

"""
0 to print out all possible options and their defaults
1 to show two overlaid 1D hists
2 to show three TGraph ROC curves 
3 to show a TH2D with smart bin labels...fancy
"""
# which_tests = [0]
# which_tests = [1, 2, 3]
which_tests = [2]

for which_test in which_tests:

    if which_test == 0:

        ply.Options().usage()

    if which_test == 1:

        h1 = r.TH1F("h1","h1",30,0,5)
        h1.FillRandom("gaus",4000)

        h2 = r.TH1F("h2","h2",30,0,5)
        h2.FillRandom("expo",4000)

        h3 = r.TH1F("h3","h3",15,2.5,5)
        h3.FillRandom("gaus",1500)

        ply.plot_hist(
                bgs=[h1,h2,h3],
                colors = [r.kRed-2, r.kAzure+2, r.kGreen-2],
                legend_labels = ["first", "second", "third"],
                options = {
                    "do_stack": False,
                    "output_name": "test1.pdf",
                    "legend_percentageinbox": True,
                    "cms_label": "Preliminary",
                    "lumi_value": 1.,
                    "output_ic": True,
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
                legend_labels = ["red", "white", "blue"],
                options = {
                    "legend_alignment": "bottom right",
                    "legend_scalex": 0.4,
                    "legend_scaley": 0.8,
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
                    "output_ic": True,
                    }
                )


