import os
import ROOT as r
import numpy as np
import utils
import array
from math import log

r.gROOT.SetBatch(1) # please don't open a window
r.gErrorIgnoreLevel = r.kWarning # ignore Info messages when saving pdfs, for example

class Options(object):

    def __init__(self, options={}, kind=None):

        self.options = options
        self.kind = kind

        self.recognized_options = {

            # Legend
            "legend_coordinates": { "type": "List", "desc": "4 elements specifying TLegend constructor coordinates", "default": [0.65,0.70,0.93,0.87], "kinds": ["1d","1dratio","graph"], },
            "legend_alignment": { "type": "Boolean", "desc": "easy alignment of TLegend. String containing two words from: bottom, top, left, right", "default": "", "kinds": ["1d","1dratio","graph"], },
            "legend_opacity": { "type": "Float", "desc": "from 0 to 1 representing the opacity of the TLegend white background", "default": 0, "kinds": ["1d","1dratio","graph"], },
  # TODO    "legend_percentageinbox": { "type": "Boolean", "desc": "show relative process contributions as %age in the legend thumbnails", "default": False, "kinds": ["1d","1dratio"], },

            # Axes
            "xaxis_log": { "type": "Boolean", "desc": "log scale x-axis", "default": False, "kinds": ["1d","1dratio","graph","2d"], },
            "yaxis_log": { "type": "Boolean", "desc": "log scale y-axis", "default": False, "kinds": ["1d","1dratio","graph","2d"], },
            "zaxis_log": { "type": "Boolean", "desc": "log scale z-axis", "default": False, "kinds": ["2d"], },

            "xaxis_label": { "type": "String", "desc": "label for x axis", "default": "x title", "kinds": ["1d","1dratio","graph","2d"], },
            "yaxis_label": { "type": "String", "desc": "label for y axis", "default": "y title", "kinds": ["1d","1dratio","graph","2d"], },
            "zaxis_label": { "type": "String", "desc": "label for z axis", "default": "", "kinds": ["2d"], },

            "xaxis_moreloglabels": { "type": "Boolean", "desc": "show denser labels with logscale for x axis", "default": False, "kinds": ["1d","1dratio","graph","2d"], },
            "yaxis_moreloglabels": { "type": "Boolean", "desc": "show denser labels with logscale for y axis", "default": False, "kinds": ["1d","1dratio","graph","2d"], },
            "xaxis_noexponents": { "type": "Boolean", "desc": "don't show exponents in logscale labels for x axis", "default": False, "kinds": ["1d","1dratio","graph","2d"], },
            "yaxis_noexponents": { "type": "Boolean", "desc": "don't show exponents in logscale labels for y axis", "default": False, "kinds": ["1d","1dratio","graph","2d"], },

            "xaxis_range": { "type": "List", "desc": "2 elements to specify x axis range", "default": [], "kinds": ["1d","1dratio","graph","2d"], },
            "yaxis_range": { "type": "List", "desc": "2 elements to specify y axis range", "default": [], "kinds": ["1d","1dratio","graph","2d"], },
            "zaxis_range": { "type": "List", "desc": "2 elements to specify z axis range", "default": [], "kinds": ["2d"], },

            # Overall
            "title": { "type": "String", "desc": "plot title", "default": "Plot", "kinds": ["1d","1dratio","graph","2d"], },
            "draw_option_2d": { "type": "String", "desc": "hist draw option", "default": "colz", "kinds": ["2d"], },

            # Misc
            "do_stack": { "type": "Boolean", "desc": "stack histograms", "default": True, "kinds": ["1d","1dratio"], },
            "palette_name": { "type": "String", "desc": "color palette: 'default', 'rainbow', 'susy', etc.", "default": "default", "kinds": ["2d"], },

            "bin_text_size": { "type": "Float", "desc": "size of text in bins (TH2::SetMarkerSize)", "default": 1.7, "kinds": ["2d"], },
            "bin_text_format": { "type": "String", "desc": "format string for text in TH2 bins", "default": ".1f", "kinds": ["2d"], },
            "bin_text_smart": { "type": "Boolean", "desc": "change bin text color for aesthetics", "default": False, "kinds": ["2d"], },
            "bin_text_format_smart": { "type": "String", "desc": "python-syntax format string for smart text in TH2 bins taking value and bin error", "default": "{0:.0f}#pm{1:.0f}", "kinds": ["2d"], },

            # Fun
            "us_flag": { "type": "Boolean", "desc": "show the US flag in the corner", "default": False, "kinds": ["1d","1dratio","graph","2d"], },
            "us_flag_coordinates": { "type": "List", "desc": "Specify flag location with (x pos, y pos, size)", "default": [0.90,0.95,0.10], "kinds": ["1d","1dratio","graph","2d"], },

            # Output
            "output_name": { "type": "String", "desc": "output file name/path", "default": "plot.pdf", "kinds": ["1d","1dratio","graph","2d"], },

        }

        self.check_options()

    def usage(self):

        for key,obj in self.recognized_options.items():
            default = obj["default"]
            desc = obj["desc"]
            typ = obj["type"]
            kinds = obj["kinds"]
            if self.kind and self.kind not in kinds: continue
            if type(default) is str: default = '"{}"'.format(default)
            print "* {} [{}]\n    {} (default: {})".format(key,typ,desc,default)



    def check_options(self):
        for name,val in self.options.items():
            if name not in self.recognized_options:
                print ">>> Option {} not in list of recognized options".format(name)
            else:
                obj = self.recognized_options[name]
                if self.kind not in obj["kinds"]:
                    print ">>> Option {} isn't declared to work with plot type of '{}'".format(name, self.kind)
                else:
                    pass
                    # print ">>> Carry on mate ... {} is fine".format(name)



    def __getitem__(self, key):
        if key in self.options:
            return self.options[key]
        else:
            if key in self.recognized_options:
                return self.recognized_options[key]["default"]
            else:
                print ">>> Hmm, can't find {} anywhere. Typo or intentional?".format(key)
                return None

    def get(self, key, default=None):
        val = self.__getitem__(key)
        if not val: return default
        else: return val

    def __setitem__(self, key, value):
        self.options[key] = value

    def __repr__(self):
        return str(self.options)

    def __contains__(self, key):
        return key in self.options


def plot_graph(valpairs,colors=[],legend_labels=[],xlabel="",ylabel="",title="Graph",legend_position="top right",\
        logx=False,logy=False,draw_styles=[],xlims=[],ylims=[],save_as="test.pdf",options={}):

    opts = Options(options, kind="graph")

    utils.set_style()

    c1 = r.TCanvas()
    legend = get_legend(opts)

    mg = r.TMultiGraph()
    for ipair,(xs,ys) in enumerate(valpairs):
        graph = r.TGraph(len(xs), np.array(xs,dtype=float), np.array(ys,dtype=float))
        if ipair < len(colors): 
            graph.SetLineColor(colors[ipair])
            graph.SetLineWidth(4)
            graph.SetMarkerColor(colors[ipair])
            graph.SetMarkerSize(1.0)
        if ipair < len(draw_styles):
            graph.SetLineStyle(draw_styles[ipair])
        if ipair < len(legend_labels):
            legend.AddEntry(graph, legend_labels[ipair], "L")
        mg.Add(graph)

    mg.SetTitle(title)

    mg.Draw("AL")

    if opts["xaxis_range"]: mg.GetXaxis().SetRangeUser(*opts["xaxis_range"])
    if opts["yaxis_range"]: mg.GetYaxis().SetRangeUser(*opts["yaxis_range"])
    mg.GetXaxis().SetTitle(opts["xaxis_label"])
    mg.GetYaxis().SetTitle(opts["yaxis_label"])

    legend.Draw()

    if opts["xaxis_log"]:
        c1.SetLogx(1)
        mg.GetXaxis().SetMoreLogLabels(opts["xaxis_moreloglabels"])
        mg.GetXaxis().SetNoExponent(opts["xaxis_noexponents"])
    if opts["yaxis_log"]:
        c1.SetLogy(1)
        mg.GetYaxis().SetMoreLogLabels(opts["yaxis_moreloglabels"])
        mg.GetYaxis().SetNoExponent(opts["yaxis_noexponents"])

    if opts["us_flag"]:
        utils.draw_flag(c1,*opts["us_flag_coordinates"])

    save(c1, opts)

    return c1

def get_legend(opts):
    x1,y1,x2,y2 = opts["legend_coordinates"]
    legend_alignment = opts["legend_alignment"]
    if "bottom" in legend_alignment: y1, y2 = 0.18, 0.45
    if "top" in legend_alignment: y1, y2 = 0.63, 0.88
    if "left" in legend_alignment: x1, x2 = 0.18, 0.38
    if "right" in legend_alignment: x1, x2 = 0.48, 0.93
    legend = r.TLegend(x1,y1,x2,y2)
    if opts["legend_opacity"] == 1:
        legend.SetFillStyle(0)
    else:
        legend.SetFillColorAlpha(r.kWhite,1.0-opts["legend_opacity"])
    legend.SetBorderSize(1)
    legend.SetTextFont(42)
    return legend


def plot_hist(bgs=[],colors=[],legend_labels=[],options={}):

    opts = Options(options, kind="1d")

    utils.set_style()

    c1 = r.TCanvas()

    legend = get_legend(opts)

    stack = r.THStack("stack", "stack")
    for ibg,bg in enumerate(bgs):
        if ibg < len(colors): 
            # bg.SetLineColor(colors[ibg])
            bg.SetLineColor(r.TColor.GetColorDark(colors[ibg]))
            bg.SetLineWidth(1)
            bg.SetMarkerColor(colors[ibg])
            bg.SetMarkerSize(0)
            bg.SetFillColorAlpha(colors[ibg],1 if opts["do_stack"] else 0.5)
        if ibg < len(legend_labels):
            legend.AddEntry(bg, legend_labels[ibg], "F")
        stack.Add(bg)

    stack.SetTitle(opts["title"])

    stack.Draw("hist" if opts["do_stack"] else "nostackhist")

    stack.GetXaxis().SetTitle(opts["xaxis_label"])
    stack.GetYaxis().SetTitle(opts["yaxis_label"])

    legend.Draw()

    if opts["xaxis_log"]:
        c1.SetLogx(1)
        stack.GetXaxis().SetMoreLogLabels(opts["xaxis_moreloglabels"])
        stack.GetXaxis().SetNoExponent(opts["xaxis_noexponents"])
    if opts["yaxis_log"]:
        c1.SetLogy(1)
        stack.GetYaxis().SetMoreLogLabels(opts["yaxis_moreloglabels"])
        stack.GetYaxis().SetNoExponent(opts["yaxis_noexponents"])

    if opts["us_flag"]:
        utils.draw_flag(c1,*opts["us_flag_coordinates"])

    save(c1, opts)

    return c1

def draw_smart_2d_bin_labels(hist,opts):
    darknesses = [] # darkness values
    lights = [] # lighter colors
    darks = [] # darker colors
    ncolors = r.gStyle.GetNumberContours()
    for ic in range(ncolors):
        code = r.gStyle.GetColorPalette(ic)
        color = r.gROOT.GetColor(code)
        red = color.GetRed()
        green = color.GetGreen()
        blue = color.GetBlue()
        darks.append(r.TColor.GetColorDark(code))
        lights.append(r.TColor.GetColorBright(code))
        darkness = 1.0 - (0.299*red + 0.587*green + 0.114*blue)
        darknesses.append(darkness)
    labels = []
    zlow, zhigh = max(1,hist.GetMinimum()), hist.GetMaximum()
    if opts["zaxis_range"]: zlow, zhigh = opts["zaxis_range"]
    t = r.TLatex()
    t.SetTextAlign(22)
    t.SetTextSize(0.025)
    fmt = opts["bin_text_format_smart"]
    for ix in range(1,hist.GetNbinsX()+1):
        for iy in range(1,hist.GetNbinsY()+1):
            xcent = hist.GetXaxis().GetBinCenter(ix)
            ycent = hist.GetYaxis().GetBinCenter(iy)
            val = hist.GetBinContent(ix,iy)
            err = hist.GetBinError(ix,iy)
            if val == 0: continue
            if opts["zaxis_log"]:
                frac = (log(min(val,zhigh))-log(zlow))/(log(zhigh)-log(zlow))
            else:
                frac = (min(val,zhigh)-zlow)/(zhigh-zlow)
            if frac > 1.: continue
            idx = int(frac*(len(darknesses)-1))
            if darknesses[idx] < 0.7:
                t.SetTextColor(r.kBlack)
            else:
                t.SetTextColor(r.kWhite)
            # t.SetTextColor(darks[idx])
            t.DrawLatex(xcent,ycent,fmt.format(val,err))
            labels.append(t)

def set_palette(style, palette):
    if palette == "default":
        style.SetPalette(r.kBird) # default
        style.SetNumberContours(128)
    elif palette == "rainbow":
        style.SetPalette(r.kRainBow) # blue to red
        style.SetNumberContours(128)
    elif palette == "susy": 
        stops = array.array('d', [0.00, 0.34, 0.61, 0.84, 1.00])
        red   = array.array('d', [0.50, 0.50, 1.00, 1.00, 1.00])
        green = array.array('d', [0.50, 1.00, 1.00, 0.60, 0.50])
        blue  = array.array('d', [1.00, 1.00, 0.50, 0.40, 0.50])
        r.TColor.CreateGradientColorTable(len(stops), stops, red, green, blue, 255)
        # print get_luminosities(len(stops), stops, red, green, blue, 255)
        style.SetNumberContours(255)

def plot_hist_2d(hist,options={}):

    opts = Options(options, kind="2d")

    style = utils.set_style()
    style.SetPadBottomMargin(0.12)
    style.SetPadRightMargin(0.12)
    style.SetPadLeftMargin(0.10)

    set_palette(style, opts["palette_name"])

    c1 = r.TCanvas()

    hist.SetTitle(opts["title"])

    if opts["xaxis_log"]: c1.SetLogx(1)
    if opts["yaxis_log"]: c1.SetLogy(1)
    if opts["zaxis_log"]: c1.SetLogz(1)

    if opts["us_flag"]:
        utils.draw_flag(c1,*opts["us_flag_coordinates"])

    hist.Draw(opts["draw_option_2d"])
    c1.Update()

    hist.GetXaxis().SetTitle(opts["xaxis_label"])
    hist.GetYaxis().SetTitle(opts["yaxis_label"])
    hist.GetZaxis().SetTitle(opts["zaxis_label"])
    if opts["xaxis_range"]: hist.GetXaxis().SetRangeUser(*opts["xaxis_range"])
    if opts["yaxis_range"]: hist.GetYaxis().SetRangeUser(*opts["yaxis_range"])
    if opts["zaxis_range"]: hist.GetZaxis().SetRangeUser(*opts["zaxis_range"])

    hist.SetMarkerSize(opts["bin_text_size"])
    style.SetPaintTextFormat(opts["bin_text_format"])

    if opts["bin_text_smart"]:
        draw_smart_2d_bin_labels(hist, opts)

    if opts["us_flag"]:
        utils.draw_flag(c1,*opts["us_flag_coordinates"])

    save(c1, opts)

def save(c1, opts):

    print ">>> Saving {}".format(opts["output_name"])
    c1.SaveAs(opts["output_name"])


def interpolate_colors_rgb(first, second, ndiv, _persist=[]):
    colorcodes = []
    for rgb in utils.interpolate_tuples(first,second,ndiv):
        index = r.TColor.GetFreeColorIndex()
        _persist.append(r.TColor(index, *rgb))
        colorcodes.append(index)
    return colorcodes

if __name__ == "__main__":

    pass
