# coding: utf-8

import os
import ROOT as r
import utils
from array import array

r.gROOT.SetBatch(1) # please don't open a window
r.gErrorIgnoreLevel = r.kWarning # ignore Info messages when saving pdfs, for example

class Options(object):

    def __init__(self, options={}, kind=None):

        self.options = options
        self.kind = kind

        self.recognized_options = {

            # Legend
            "legend_coordinates": { "type": "List", "desc": "4 elements specifying TLegend constructor coordinates", "default": [0.63,0.67,0.93,0.87], "kinds": ["1d","1dratio","graph"], },
            "legend_alignment": { "type": "Boolean", "desc": "easy alignment of TLegend. String containing two words from: bottom, top, left, right", "default": "", "kinds": ["1d","1dratio","graph"], },
            "legend_scalex": { "type": "Float", "desc": "scale width of legend by this factor", "default": 1, "kinds": ["1d","1dratio","graph"], },
            "legend_scaley": { "type": "Float", "desc": "scale height of legend by this factor", "default": 1, "kinds": ["1d","1dratio","graph"], },
            "legend_opacity": { "type": "Float", "desc": "from 0 to 1 representing the opacity of the TLegend white background", "default": 0, "kinds": ["1d","1dratio","graph"], },
            "legend_percentageinbox": { "type": "Boolean", "desc": "show relative process contributions as %age in the legend thumbnails", "default": False, "kinds": ["1d","1dratio"], },

            # Axes
            "xaxis_log": { "type": "Boolean", "desc": "log scale x-axis", "default": False, "kinds": ["1d","1dratio","graph","2d"], },
            "yaxis_log": { "type": "Boolean", "desc": "log scale y-axis", "default": False, "kinds": ["1d","1dratio","graph","2d"], },
            "zaxis_log": { "type": "Boolean", "desc": "log scale z-axis", "default": False, "kinds": ["2d"], },

            "xaxis_label": { "type": "String", "desc": "label for x axis", "default": "x title", "kinds": ["1d","1dratio","graph","2d"], },
            "yaxis_label": { "type": "String", "desc": "label for y axis", "default": "y title", "kinds": ["1d","1dratio","graph","2d"], },
            "zaxis_label": { "type": "String", "desc": "label for z axis", "default": "", "kinds": ["2d"], },

            "xaxis_moreloglabels": { "type": "Boolean", "desc": "show denser labels with logscale for x axis", "default": False, "kinds": ["1d","1dratio","graph","2d"], },
            "yaxis_moreloglabels": { "type": "Boolean", "desc": "show denser labels with logscale for y axis", "default": False, "kinds": ["1d","1dratio","graph","2d"], },
            "zaxis_moreloglabels": { "type": "Boolean", "desc": "show denser labels with logscale for z axis", "default": False, "kinds": ["1d","1dratio","graph","2d"], },
            "xaxis_noexponents": { "type": "Boolean", "desc": "don't show exponents in logscale labels for x axis", "default": False, "kinds": ["1d","1dratio","graph","2d"], },
            "yaxis_noexponents": { "type": "Boolean", "desc": "don't show exponents in logscale labels for y axis", "default": False, "kinds": ["1d","1dratio","graph","2d"], },
            "zaxis_noexponents": { "type": "Boolean", "desc": "don't show exponents in logscale labels for z axis", "default": False, "kinds": ["1d","1dratio","graph","2d"], },

            "xaxis_range": { "type": "List", "desc": "2 elements to specify x axis range", "default": [], "kinds": ["1d","1dratio","graph","2d"], },
            "yaxis_range": { "type": "List", "desc": "2 elements to specify y axis range", "default": [], "kinds": ["1d","1dratio","graph","2d"], },
            "zaxis_range": { "type": "List", "desc": "2 elements to specify z axis range", "default": [], "kinds": ["2d"], },

            # Overall
            "title": { "type": "String", "desc": "plot title", "default": "Plot", "kinds": ["1d","1dratio","graph","2d"], },
            "draw_option_2d": { "type": "String", "desc": "hist draw option", "default": "colz", "kinds": ["2d"], },

            # CMS things
            "cms_label": {"type": "String", "desc": "E.g., 'Preliminary'; default hides label", "default": None, "kinds": ["1d","1dratio","graph","2d"]},
            "lumi_value": {"type": "String", "desc": "E.g., 35.9; default hides lumi label", "default": "", "kinds": ["1d","1dratio","graph","2d"]},
            "lumi_unit": {"type": "String", "desc": "Unit for lumi label", "default": "fb", "kinds": ["1d","1dratio","graph","2d"]},

            # Misc
            "do_stack": { "type": "Boolean", "desc": "stack histograms", "default": True, "kinds": ["1d","1dratio"], },
            "palette_name": { "type": "String", "desc": "color palette: 'default', 'rainbow', 'susy', etc.", "default": "default", "kinds": ["2d"], },

            "bin_text_size": { "type": "Float", "desc": "size of text in bins (TH2::SetMarkerSize)", "default": 1.7, "kinds": ["2d"], },
            "bin_text_format": { "type": "String", "desc": "format string for text in TH2 bins", "default": ".1f", "kinds": ["2d"], },
            "bin_text_smart": { "type": "Boolean", "desc": "change bin text color for aesthetics", "default": False, "kinds": ["2d"], },
            "bin_text_format_smart": { "type": "String", "desc": "python-syntax format string for smart text in TH2 bins taking value and bin error", "default": "{0:.0f}#pm{1:.0f}", "kinds": ["2d"], },

            "hist_line_none": { "type": "Boolean", "desc": "No lines for histograms, only fill", "default": False, "kinds": ["1d","1dratio"], },
            "hist_line_black": { "type": "Boolean", "desc": "Black lines for histograms", "default": False, "kinds": ["1d","1dratio"], },

            # Fun
            "us_flag": { "type": "Boolean", "desc": "show the US flag in the corner", "default": False, "kinds": ["1d","1dratio","graph","2d"], },
            "us_flag_coordinates": { "type": "List", "desc": "Specify flag location with (x pos, y pos, size)", "default": [0.90,0.95,0.10], "kinds": ["1d","1dratio","graph","2d"], },

            # Output
            "output_name": { "type": "String", "desc": "output file name/path", "default": "plot.pdf", "kinds": ["1d","1dratio","graph","2d"], },
            "output_ic": { "type": "Boolean", "desc": "run `ic` (imgcat) on output", "default": False, "kinds": ["1d","1dratio","graph","2d"], },

        }

        self.check_options()

    def usage(self):

        for key,obj in sorted(self.recognized_options.items()):
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


def plot_graph(valpairs,colors=[],legend_labels=[],draw_styles=[],options={}):

    opts = Options(options, kind="graph")

    utils.set_style()

    c1 = r.TCanvas()
    legend = get_legend(opts)

    mg = r.TMultiGraph()
    drawopt = ""
    for parts in enumerate(valpairs):
        ipair = parts[0]
        rest = parts[1]
        typ = "xy"
        drawopt = "AL"
        if len(rest) == 2:
            xs, ys = rest
            graph = r.TGraphAsymmErrors(len(xs), array('d',xs), array('d',ys))
            typ = "xy"
            legopt = "LP"
        elif len(rest) == 4:
            xs, ys, ylows, yhighs = rest
            zeros = array('d',[0. for _ in xs])
            graph = r.TGraphAsymmErrors(len(xs), array('d',xs), array('d',ys), zeros, zeros, array('d',ylows),array('d',yhighs))
            typ = "xyey"
            legopt, drawopt = "FLP","ALP3"
        elif len(rest) == 6:
            xs, ys, xlows, xhighs, ylows, yhighs = rest
            graph = r.TGraphAsymmErrors(len(xs), array('d',xs), array('d',ys), array('d',xlows), array('d',xhighs), array('d',ylows),array('d',yhighs))
            typ = "xyexey"
            legopt, drawopt = "FELP","ALP3"
        else:
            raise ValueError("don't recognize this format")

        if ipair < len(colors): 
            graph.SetLineColor(colors[ipair])
            graph.SetLineWidth(4)
            graph.SetMarkerColor(colors[ipair])
            graph.SetMarkerSize(0.30*graph.GetLineWidth())
        if ipair < len(draw_styles):
            graph.SetLineStyle(draw_styles[ipair])
        if ipair < len(legend_labels):
            legend.AddEntry(graph, legend_labels[ipair],legopt)

        if typ in ["xyey","xyexey"]:
            graph.SetFillColorAlpha(graph.GetLineColor(),0.3)

        mg.Add(graph)

    mg.SetTitle(opts["title"])

    mg.Draw(drawopt)

    if legend_labels: legend.Draw()

    draw_cms_lumi(c1, opts)
    handle_axes(c1, mg, opts)
    draw_extra_stuff(c1, opts)
    save(c1, opts)

    return c1

def get_legend(opts):
    x1,y1,x2,y2 = opts["legend_coordinates"]
    legend_alignment = opts["legend_alignment"]
    if "bottom" in legend_alignment: y1, y2 = 0.18, 0.38
    if "top" in legend_alignment: y1, y2 = 0.67, 0.87
    if "left" in legend_alignment: x1, x2 = 0.18, 0.48
    if "right" in legend_alignment: x1, x2 = 0.63, 0.93

    # scale width and height of legend keeping the sides
    # closest to the plot edges the same (so we expand/contact the legend inwards)
    scalex = opts["legend_scalex"]
    scaley = opts["legend_scaley"]
    toshift_x = (1.-scalex)*(x2-x1)
    toshift_y = (1.-scaley)*(y2-y1)
    if 0.5*(x1+x2) > 0.5: # second half, so keep the right side stationary
        x1 += toshift_x
    else: # keep left side pinned
        x2 -= toshift_x
    if 0.5*(y1+y2) > 0.5: # upper half, so keep the upper side stationary
        y1 += toshift_y
    else: # keep bottom side pinned
        y2 -= toshift_y

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

    # sort backgrounds, but make sure all parameters have same length
    if len(colors) < len(bgs):
        print ">>> Provided only {} colors for {} backgrounds, so using defalt palette".format(len(colors),len(bgs))
        colors = utils.get_default_colors()
    if len(legend_labels) < len(bgs):
        print ">>> Provided only {} legend_labels for {} backgrounds, so using hist titles".format(len(legend_labels),len(bgs))
        for ibg in range(len(bgs)-len(legend_labels)):
            legend_labels.append(bgs[ibg].GetTitle())
    sort_methods = {
            "INTEGRAL_DESCENDING": lambda x: -x[0].Integral(),
            "INTEGRAL_ASCENDING": lambda x: x[0].Integral(),
            }
    which_method = "INTEGRAL_ASCENDING"
    bgs, colors, legend_labels = zip(*sorted(zip(bgs,colors,legend_labels), key=sort_methods[which_method]))

    stack = r.THStack("stack", "stack")
    for ibg,bg in enumerate(bgs):
        if ibg < len(colors): 
            bg.SetLineColor(r.TColor.GetColorDark(colors[ibg]))
            if opts["hist_line_black"]:
                bg.SetLineColor(r.kBlack)
            bg.SetLineWidth(1)
            bg.SetMarkerColor(colors[ibg])
            bg.SetMarkerSize(0)
            bg.SetFillColorAlpha(colors[ibg],1 if opts["do_stack"] else 0.5)
            if opts["hist_line_none"]:
                bg.SetLineWidth(0)
        if ibg < len(legend_labels):
            legend.AddEntry(bg, legend_labels[ibg], "F")
        stack.Add(bg)

    stack.SetTitle(opts["title"])

    stack.Draw("hist" if opts["do_stack"] else "nostackhist")

    legend.Draw()

    if opts["legend_percentageinbox"]:
        t = r.TLatex()
        t.SetTextAlign(22)
        t.SetTextColor(r.kWhite)
        # t.SetTextColor(r.kBlack)
        info = utils.get_legend_marker_info(legend)
        t.SetTextSize(info["label_height"])
        total_integral = sum(bg.Integral() for bg in bgs)
        # we want the number to be centered, without the % symbol, so nudge the percentage text right a bit
        nudge_right = info["box_width"]*0.15
        for icoord, (xndc, yndc) in enumerate(info["coords"]):
            bg = bgs[icoord]
            percentage = int(100.0*bg.Integral()/total_integral)
            color = r.gROOT.GetColor(bg.GetFillColor())
            red = color.GetRed()
            green = color.GetGreen()
            blue = color.GetBlue()
            darkness = utils.compute_darkness(red, green, blue)
            if darkness < 0.5:
                t.SetTextColor(r.kBlack)
            else: 
                t.SetTextColor(r.kWhite)
            # t.SetTextColor(r.TColor.GetColorDark(bg.GetFillColor()))
            t.DrawLatexNDC(xndc+nudge_right,yndc,"%i#scale[0.5]{#lower[-0.2]{%%}}" % (percentage))

    draw_cms_lumi(c1, opts)
    handle_axes(c1, stack, opts)
    draw_extra_stuff(c1, opts)
    save(c1, opts)

    return c1

def handle_axes(c1, obj, opts):
    if opts["xaxis_log"]:
        c1.SetLogx(1)
        obj.GetXaxis().SetMoreLogLabels(opts["xaxis_moreloglabels"])
        obj.GetXaxis().SetNoExponent(opts["xaxis_noexponents"])
    if opts["yaxis_log"]:
        c1.SetLogy(1)
        obj.GetYaxis().SetMoreLogLabels(opts["yaxis_moreloglabels"])
        obj.GetYaxis().SetNoExponent(opts["yaxis_noexponents"])
    if opts["zaxis_log"] and hasattr(obj, "GetZaxis"):
        c1.SetLogz(1)
        obj.GetZaxis().SetMoreLogLabels(opts["zaxis_moreloglabels"])
        obj.GetZaxis().SetNoExponent(opts["zaxis_noexponents"])

    obj.GetXaxis().SetTitle(opts["xaxis_label"])
    if opts["xaxis_range"]: obj.GetXaxis().SetRangeUser(*opts["xaxis_range"])

    obj.GetYaxis().SetTitle(opts["yaxis_label"])
    if opts["yaxis_range"]: obj.GetYaxis().SetRangeUser(*opts["yaxis_range"])

    if hasattr(obj, "GetZaxis"):
        obj.GetZaxis().SetTitle(opts["zaxis_label"])
        if opts["zaxis_range"]: obj.GetZaxis().SetRangeUser(*opts["zaxis_range"])


def plot_hist_2d(hist,options={}):

    opts = Options(options, kind="2d")

    style = utils.set_style_2d()

    utils.set_palette(style, opts["palette_name"])

    c1 = r.TCanvas()

    hist.Draw(opts["draw_option_2d"])

    hist.SetTitle(opts["title"])

    hist.SetMarkerSize(opts["bin_text_size"])
    style.SetPaintTextFormat(opts["bin_text_format"])

    if opts["bin_text_smart"]:
        utils.draw_smart_2d_bin_labels(hist, opts)

    draw_cms_lumi(c1, opts)
    handle_axes(c1, hist, opts)
    draw_extra_stuff(c1, opts)
    save(c1, opts)

def draw_cms_lumi(c1, opts, _persist=[]):
    t = r.TLatex()
    t.SetTextAlign(11) # align bottom left corner of text
    t.SetTextColor(r.kBlack)
    t.SetTextSize(0.04)
    # get top left corner of current pad, and nudge up the y coord a bit
    xcms = r.gPad.GetX1() + r.gPad.GetLeftMargin()
    ycms = r.gPad.GetY2() - r.gPad.GetTopMargin() + 0.01
    xlumi = r.gPad.GetX2() - r.gPad.GetRightMargin()
    cms_label = opts["cms_label"]
    lumi_value = str(opts["lumi_value"])
    lumi_unit = opts["lumi_unit"]
    energy = 13
    if cms_label is not None:
        t.DrawLatexNDC(xcms,ycms,"#scale[1.25]{#font[61]{CMS}} #scale[1.1]{#font[52]{%s}}" % cms_label)
    if lumi_value:
        t.SetTextSize(0.04)
        t.SetTextAlign(31) # align bottom right
        t.SetTextFont(42) # align bottom right
        t.DrawLatexNDC(xlumi,ycms,"{lumi_str} {lumi_unit}^{{-1}} ({energy} TeV)".format(energy=energy, lumi_str=lumi_value, lumi_unit=lumi_unit))
    _persist.append(t)

def draw_extra_stuff(c1, opts):
    if opts["us_flag"]:
        utils.draw_flag(c1,*opts["us_flag_coordinates"])

def save(c1, opts):

    fname = opts["output_name"]
    print ">>> Saving {}".format(fname)
    c1.SaveAs(fname)
    if opts["output_ic"]:
        os.system("ic {}".format(fname))



if __name__ == "__main__":

    pass
    h1 = r.TH1F("h1","h1",30,0,5)
    h1.FillRandom("gaus",4000)
    h2 = r.TH1F("h2","h2",30,0,5)
    h2.FillRandom("expo",3000)
    h3 = r.TH1F("h3","h3",15,2.5,5)
    h3.FillRandom("gaus",1500)
    plot_hist(
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

    # xyg = r.TF2("xygaus","xygaus",0,10,0,10);
    # xyg.SetParameters(1,5,2,5,2)  # amplitude, meanx,sigmax,meany,sigmay
    # h2 = r.TH2F("h2","h2",10,0,10, 10,0,10)
    # h2.FillRandom("xygaus",10000)
    # plot_hist_2d(
    #         h2,
    #         options = {
    #             "zaxis_log": True,
    #             "output_name": "test.pdf",
    #             "bin_text_smart": True,
    #             "zaxis_moreloglabels": True,
    #             "zaxis_noexponents": True,
    #             "output_name": "test3.pdf",
    #             "us_flag": False,
    #             "output_ic": True,
    #             "cms_label": "",
    #             "lumi_value": 35.9,
    #             }
    #         )


