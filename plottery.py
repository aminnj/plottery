# coding: utf-8

import os
import ROOT as r
import utils
from array import array
import math
from itertools import cycle

r.gROOT.SetBatch(1) # please don't open a window
r.gErrorIgnoreLevel = r.kError # ignore Info/Warnings

class Options(object):

    def __init__(self, options={}, kind=None):

        self.options = options
        self.kind = kind

        self.recognized_options = {

            # Legend
            "legend_coordinates": { "type": "List", "desc": "4 elements specifying TLegend constructor coordinates", "default": [0.63,0.67,0.93,0.87], "kinds": ["1dratio","graph"], },
            "legend_alignment": { "type": "Boolean", "desc": "easy alignment of TLegend. String containing two words from: bottom, top, left, right", "default": "", "kinds": ["1dratio","graph"], },
            "legend_smart": { "type": "Boolean", "desc": "Smart alignment of legend to prevent overlaps", "default": False, "kinds": ["1dratio"], },
            "legend_border": { "type": "Boolean", "desc": "show legend border?", "default": True, "kinds": ["1dratio","graph"], },
            "legend_scalex": { "type": "Float", "desc": "scale width of legend by this factor", "default": 1, "kinds": ["1dratio","graph"], },
            "legend_scaley": { "type": "Float", "desc": "scale height of legend by this factor", "default": 1, "kinds": ["1dratio","graph"], },
            "legend_opacity": { "type": "Float", "desc": "from 0 to 1 representing the opacity of the TLegend white background", "default": 0, "kinds": ["1dratio","graph"], },
            "legend_ncolumns": { "type": "Int", "desc": "number of columns in the legend", "default": 1, "kinds": ["1dratio","graph"], },
            "legend_percentageinbox": { "type": "Boolean", "desc": "show relative process contributions as %age in the legend thumbnails", "default": False, "kinds": ["1dratio"], },

            # Axes
            "xaxis_log": { "type": "Boolean", "desc": "log scale x-axis", "default": False, "kinds": ["1dratio","graph","2d"], },
            "yaxis_log": { "type": "Boolean", "desc": "log scale y-axis", "default": False, "kinds": ["1dratio","graph","2d"], },
            "zaxis_log": { "type": "Boolean", "desc": "log scale z-axis", "default": False, "kinds": ["2d"], },

            "xaxis_label": { "type": "String", "desc": "label for x axis", "default": "x title", "kinds": ["1dratio","graph","2d"], },
            "yaxis_label": { "type": "String", "desc": "label for y axis", "default": "Events", "kinds": ["1dratio","graph","2d"], },
            "zaxis_label": { "type": "String", "desc": "label for z axis", "default": "", "kinds": ["2d"], },

            "xaxis_moreloglabels": { "type": "Boolean", "desc": "show denser labels with logscale for x axis", "default": False, "kinds": ["1dratio","graph","2d"], },
            "yaxis_moreloglabels": { "type": "Boolean", "desc": "show denser labels with logscale for y axis", "default": False, "kinds": ["1dratio","graph","2d"], },
            "zaxis_moreloglabels": { "type": "Boolean", "desc": "show denser labels with logscale for z axis", "default": False, "kinds": ["1dratio","graph","2d"], },
            "xaxis_noexponents": { "type": "Boolean", "desc": "don't show exponents in logscale labels for x axis", "default": False, "kinds": ["1dratio","graph","2d"], },
            "yaxis_noexponents": { "type": "Boolean", "desc": "don't show exponents in logscale labels for y axis", "default": False, "kinds": ["1dratio","graph","2d"], },
            "zaxis_noexponents": { "type": "Boolean", "desc": "don't show exponents in logscale labels for z axis", "default": False, "kinds": ["1dratio","graph","2d"], },

            "xaxis_range": { "type": "List", "desc": "2 elements to specify x axis range", "default": [], "kinds": ["1dratio","graph","2d"], },
            "yaxis_range": { "type": "List", "desc": "2 elements to specify y axis range", "default": [], "kinds": ["1dratio","graph","2d"], },
            "zaxis_range": { "type": "List", "desc": "2 elements to specify z axis range", "default": [], "kinds": ["2d"], },

            # Ratio
            "ratio_name": { "type": "String", "desc": "name of ratio pad", "default": "Data/MC", "kinds": ["1dratio"], },
            "ratio_range": { "type": "List", "desc": "pair for min and max y-value for ratio", "default": [0.,2.], "kinds": ["1dratio"], },
            "ratio_horizontal_lines": { "type": "List", "desc": "list of y-values to draw horizontal line", "default": [1.], "kinds": ["1dratio"], },
            "ratio_chi2prob": { "type": "Boolean", "desc": "show chi2 probability for ratio", "default": False, "kinds": ["1dratio"], },
            "ratio_pull": { "type": "Boolean", "desc": "show pulls instead of ratios in ratio pad", "default": False, "kinds": ["1dratio"], },
            "ratio_ndivisions": { "type": "Int", "desc": "SetNdivisions integer for ratio", "default": 505, "kinds": ["1dratio"], },
            "ratio_numden_indices": { "type": "List", "desc": "Pair of numerator and denominator histogram indices (from `bgs`) for ratio", "default": None, "kinds": ["1dratio"], },

            # Overall
            "title": { "type": "String", "desc": "plot title", "default": "", "kinds": ["1dratio","graph","2d"], },
            "draw_points": { "type": "Boolean", "desc": "draw points instead of fill", "default": False, "kinds": ["1d","1dratio"], },
            "draw_option_2d": { "type": "String", "desc": "hist draw option", "default": "colz", "kinds": ["2d"], },

            # CMS things
            "cms_label": {"type": "String", "desc": "E.g., 'Preliminary'; default hides label", "default": None, "kinds": ["1dratio","graph","2d"]},
            "lumi_value": {"type": "String", "desc": "E.g., 35.9; default hides lumi label", "default": "", "kinds": ["1dratio","graph","2d"]},
            "lumi_unit": {"type": "String", "desc": "Unit for lumi label", "default": "fb", "kinds": ["1dratio","graph","2d"]},

            # Misc
            "do_stack": { "type": "Boolean", "desc": "stack histograms", "default": True, "kinds": ["1dratio"], },
            "palette_name": { "type": "String", "desc": "color palette: 'default', 'rainbow', 'susy', etc.", "default": "default", "kinds": ["2d"], },
            "show_bkg_errors": { "type": "Boolean", "desc": "show error bar for background stack", "default": False, "kinds": ["1dratio"], },
            "show_bkg_smooth": { "type": "Boolean", "desc": "show smoothed background stack", "default": False, "kinds": ["1dratio"], },
            "bkg_sort_method": { "type": "Boolean", "desc": "how to sort background stack using integrals: 'unsorted', 'ascending', or 'descending'", "default": 'ascending', "kinds": ["1dratio"], },


            "bin_text_size": { "type": "Float", "desc": "size of text in bins (TH2::SetMarkerSize)", "default": 1.7, "kinds": ["2d"], },
            "bin_text_format": { "type": "String", "desc": "format string for text in TH2 bins", "default": ".1f", "kinds": ["2d"], },
            "bin_text_smart": { "type": "Boolean", "desc": "change bin text color for aesthetics", "default": False, "kinds": ["2d"], },
            "bin_text_format_smart": { "type": "String", "desc": "python-syntax format string for smart text in TH2 bins taking value and bin error", "default": "{0:.0f}#pm{1:.0f}", "kinds": ["2d"], },

            "hist_line_none": { "type": "Boolean", "desc": "No lines for histograms, only fill", "default": False, "kinds": ["1dratio"], },
            "hist_line_black": { "type": "Boolean", "desc": "Black lines for histograms", "default": False, "kinds": ["1dratio"], },
            "hist_disable_xerrors": { "type": "Boolean", "desc": "Disable the x-error bars on data for 1D hists", "default": False, "kinds": ["1dratio"], },

            "extra_text": { "type": "List", "desc": "list of strings for textboxes", "default": [], "kinds": [ "1dratio"], },
            "extra_text_xpos": { "type": "Float", "desc": "NDC x position (0 to 1) for extra text", "default": 0.2, "kinds": [ "1dratio"], },

            # Fun
            "us_flag": { "type": "Boolean", "desc": "show the US flag in the corner", "default": False, "kinds": ["1dratio","graph","2d"], },
            "us_flag_coordinates": { "type": "List", "desc": "Specify flag location with (x pos, y pos, size)", "default": [0.68,0.96,0.06], "kinds": ["1dratio","graph","2d"], },

            # Output
            "output_name": { "type": "String", "desc": "output file name/path", "default": "plot.pdf", "kinds": ["1dratio","graph","2d"], },
            "output_ic": { "type": "Boolean", "desc": "run `ic` (imgcat) on output", "default": False, "kinds": ["1dratio","graph","2d"], },
            "output_jsroot": { "type": "Boolean", "desc": "output .json for jsroot", "default": False, "kinds": ["1dratio","graph","2d"], },

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
            print "* `{}` [{}]\n    {} (default: {})".format(key,typ,desc,default)

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

    def is_default(self, key):
        """
        returns True if user has not overriden this particular option
        """
        default = None
        if key in self.recognized_options:
            default = self.recognized_options[key]["default"]
        return (self.__getitem__(key) == default)

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
        if len(rest) == 2:
            xs, ys = rest
            graph = r.TGraphAsymmErrors(len(xs), array('d',xs), array('d',ys))
            typ = "xy"
            legopt = "LP"
            drawopt = "ALP"
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
            graph.SetMarkerSize(0.20*graph.GetLineWidth())
        if ipair < len(draw_styles):
            graph.SetLineStyle(draw_styles[ipair])
        if ipair < len(legend_labels):
            legend.AddEntry(graph, legend_labels[ipair],legopt)

        if typ in ["xyey","xyexey"]:
            graph.SetFillColorAlpha(graph.GetLineColor(),0.25)

        mg.Add(graph,drawopt)

    mg.SetTitle(opts["title"])

    mg.Draw("A")

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
    if opts["legend_border"]:
        legend.SetBorderSize(1)
    else:
        legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetNColumns(opts["legend_ncolumns"])
    return legend


def plot_hist(data=None,bgs=[],legend_labels=[],colors=[],sigs=[],sig_labels=[],options={}):

    opts = Options(options, kind="1dratio")

    style = utils.set_style()

    c1 = r.TCanvas()

    has_data = data and data.InheritsFrom(r.TH1F.Class())
    do_ratio = has_data or opts["ratio_numden_indices"]
    if do_ratio:
        pad_main = r.TPad("pad1","pad1",0.0,0.18,1.0,1.0)
        pad_ratio = r.TPad("pad2","pad2",0.0, 0.00, 1.0, 0.19)
        pad_main.Draw()
        pad_ratio.Draw()
    else:
        pad_main = r.TPad("pad1","pad1",0.,0.,1.,1.)
        pad_main.Draw()

    pad_main.cd()

    # sort backgrounds, but make sure all parameters have same length
    if len(colors) < len(bgs):
        print ">>> Provided only {} colors for {} backgrounds, so using defalt palette".format(len(colors),len(bgs))
        colors = utils.get_default_colors()
    if len(legend_labels) < len(bgs):
        print ">>> Provided only {} legend_labels for {} backgrounds, so using hist titles".format(len(legend_labels),len(bgs))
        for ibg in range(len(bgs)-len(legend_labels)):
            legend_labels.append(bgs[ibg].GetTitle())
    sort_methods = {
            "descending": lambda x: -x[0].Integral(),
            "ascending": lambda x: x[0].Integral(), # highest integral on top of stack
            "unsorted": lambda x: 1, # preserve original ordering
            }
    which_method = opts["bkg_sort_method"]
    original_index_mapping = range(len(bgs))
    bgs, colors, legend_labels, original_index_mapping = zip(*sorted(zip(bgs,colors,legend_labels,original_index_mapping), key=sort_methods[which_method]))
    # map original indices of bgs to indices of sorted bgs
    original_index_mapping = { oidx: nidx for oidx,nidx in zip(original_index_mapping,range(len(bgs))) }
    map(lambda x: x.Sumw2(), bgs)

    legend = get_legend(opts)

    if has_data:
        data.SetMarkerStyle(20)
        data.SetMarkerColor(r.kBlack)
        data.SetLineWidth(2)
        data.SetMarkerSize(0.8)
        data.SetLineColor(r.kBlack)
        legend.AddEntry(data, "Data", "LPE" if not opts["hist_disable_xerrors"] else "PE")

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
            if opts["draw_points"]:
                bg.SetLineWidth(3)
                bg.SetMarkerStyle(20)
                bg.SetLineColor(colors[ibg])
                bg.SetMarkerColor(colors[ibg])
                bg.SetMarkerSize(0.8)
            if opts["hist_line_none"]:
                bg.SetLineWidth(0)
        if ibg < len(legend_labels):
            entry_style = "F"
            if opts["draw_points"]:
                entry_style = "LPE"
            legend.AddEntry(bg, legend_labels[ibg], entry_style)
        stack.Add(bg)

    stack.SetTitle(opts["title"])

    drawopt = "nostackhist"
    if opts["do_stack"]: drawopt = "hist"
    if opts["show_bkg_errors"]: drawopt += "e1"
    if opts["show_bkg_smooth"]: drawopt += "C"
    if opts["draw_points"]: drawopt += "PE"
    stack.SetMaximum(utils.get_stack_maximum(data,stack))
    stack.Draw(drawopt)
    ymax = stack.GetHistogram().GetMaximum()

    if has_data:
        if opts["hist_disable_xerrors"]: 
            style.SetErrorX(0.)
        data.Draw("samepe")

    if sigs:
        colors = cycle([r.kRed, r.kOrange-4, r.kTeal-5])
        for hsig,signame,color in zip(sigs, sig_labels,colors):
            hsig.SetMarkerStyle(1) # 2 has errors
            hsig.SetMarkerColor(color)
            hsig.SetLineWidth(3)
            hsig.SetMarkerSize(0.8)
            hsig.SetLineColor(color)
            legend.AddEntry(hsig,signame, "LPE")
            hsig.Draw("samepe")

    if opts["legend_smart"]:
        utils.smart_legend(legend, bgs, data=data, ymax=ymax)

    legend.Draw()

    if opts["legend_percentageinbox"]:
        draw_percentageinbox(legend, bgs, sigs, opts, has_data=has_data)

    draw_cms_lumi(pad_main, opts)
    handle_axes(pad_main, stack, opts)
    draw_extra_stuff(pad_main, opts)

    if do_ratio:
        pad_ratio.cd()

        if opts["ratio_numden_indices"]:
            orig_num_idx, orig_den_idx = opts["ratio_numden_indices"]
            numer = bgs[original_index_mapping[orig_num_idx]].Clone("numer")
            denom = bgs[original_index_mapping[orig_den_idx]].Clone("denom")
            if opts.is_default("ratio_name"):
                opts["ratio_name"] = "{}/{}".format(legend_labels[original_index_mapping[orig_num_idx]],legend_labels[original_index_mapping[orig_den_idx]])
        else:
            # construct numer and denom to be used everywhere
            numer = data.Clone("numer")
            denom = bgs[0].Clone("sumbgs")
            denom.Reset()
            denom = sum(bgs,denom)

        ratio = numer.Clone("ratio")
        ratio.Divide(denom)

        def get_err_div(num,den,enum,eden):
            return ((enum/den)**2.0+(eden*num/(den)**2.0)**2.0)**0.5

        if opts["ratio_pull"]:
            for ibin in range(1,ratio.GetNbinsX()+1):
                ratio_val = ratio.GetBinContent(ibin)
                ratio_err = ratio.GetBinError(ibin)
                numer_val = numer.GetBinContent(ibin)
                numer_err = numer.GetBinError(ibin)
                denom_val = denom.GetBinContent(ibin)
                denom_err = denom.GetBinError(ibin)
                # gaussian pull
                pull = (ratio_val-1.)/((numer_err**2.+denom_err**2.)**0.5)
                if numer_val > 1e-6:
                    # more correct pull, but is inf when 0 data, so fall back to gaus pull in that case
                    pull = r.RooStats.NumberCountingUtils.BinomialObsZ(numer_val,denom_val,denom_err/denom_val);
                ratio.SetBinContent(ibin,pull)
                ratio.SetBinError(ibin,0.)
            opts["ratio_range"] = [-3.0,3.0]
            opts["ratio_horizontal_line"] = 0.
            opts["ratio_ndivisions"] = 208
            opts["ratio_horizontal_lines"] = [-1.,0.,1.]


        do_style_ratio(ratio, opts)
        ratio.Draw("PE")

        ratio_horizontal_lines = opts["ratio_horizontal_lines"]
        line = r.TLine()
        line.SetLineColor(r.kGray+2);
        line.SetLineWidth(1);
        for yval in ratio_horizontal_lines:
            line.DrawLine(ratio.GetXaxis().GetBinLowEdge(1),yval,ratio.GetXaxis().GetBinUpEdge(ratio.GetNbinsX()),yval)

        if opts["ratio_chi2prob"]:
            oldpad = r.gPad
            c1.cd()
            chi2 = 0.
            for ibin in range(1,ratio.GetNbinsX()+1):
                err = ratio.GetBinError(ibin)
                val = ratio.GetBinContent(ibin)
                chi2 += (val-1.)**2./err
            prob = r.TMath.Prob(chi2,ratio.GetNbinsX()-1)
            t = r.TLatex()
            t.SetTextAlign(22)
            t.SetTextFont(42)
            t.SetTextColor(r.kBlack)
            t.SetTextSize(0.03)
            yloc = pad_ratio.GetAbsHNDC()
            t.DrawLatexNDC(0.5,yloc+0.01,"P(#chi^{{2}}/ndof) = {:.2f}".format(prob))
            oldpad.cd()

        pad_main.cd()


    save(c1, opts)

    return c1

def do_style_ratio(ratio, opts):
    ratio.SetMarkerStyle(20)
    ratio.SetMarkerSize(0.8)
    ratio.SetLineWidth(2)
    ratio.SetTitle("")
    ratio.GetYaxis().SetTitle(opts["ratio_name"])
    ratio.GetYaxis().SetTitleOffset(0.25)
    ratio.GetYaxis().SetTitleSize(0.2)
    ratio.GetYaxis().SetNdivisions(opts["ratio_ndivisions"])
    ratio.GetYaxis().SetLabelSize(0.13)
    ratio.GetYaxis().SetRangeUser(*opts["ratio_range"])
    ratio.GetXaxis().SetLabelSize(0.)
    ratio.GetXaxis().SetTickSize(0.06)

def draw_percentageinbox(legend, bgs, sigs, opts, has_data=False):
    t = r.TLatex()
    t.SetTextAlign(22)
    t.SetTextFont(42)
    t.SetTextColor(r.kWhite)
    info = utils.get_legend_marker_info(legend)
    t.SetTextSize(info["label_height"])
    all_entries = list(bgs) + list(sigs)
    total_integral = sum(bg.Integral() for bg in bgs)
    # we want the number to be centered, without the % symbol, so nudge the percentage text right a bit
    nudge_right = info["box_width"]*0.15
    for icoord, (xndc, yndc) in enumerate(info["coords"]):
        # if we have data, skip it and restart numbering from 0
        if has_data:
            if icoord == 0: continue
            icoord -= 1
        bg = all_entries[icoord]
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


def handle_axes(c1, obj, opts):

    obj.GetXaxis().SetTitle(opts["xaxis_label"])
    if opts["xaxis_range"]: obj.GetXaxis().SetRangeUser(*opts["xaxis_range"])
    if opts["xaxis_log"]:
        c1.SetLogx(1)
        obj.GetXaxis().SetMoreLogLabels(opts["xaxis_moreloglabels"])
        obj.GetXaxis().SetNoExponent(opts["xaxis_noexponents"])

    obj.GetYaxis().SetTitle(opts["yaxis_label"])
    if opts["yaxis_range"]: obj.GetYaxis().SetRangeUser(*opts["yaxis_range"])
    if opts["yaxis_log"]:
        c1.SetLogy(1)
        obj.GetYaxis().SetMoreLogLabels(opts["yaxis_moreloglabels"])
        obj.GetYaxis().SetNoExponent(opts["yaxis_noexponents"])

    if hasattr(obj, "GetZaxis"):
        obj.GetZaxis().SetTitle(opts["zaxis_label"])
        if opts["zaxis_range"]: obj.GetZaxis().SetRangeUser(*opts["zaxis_range"])
        if opts["zaxis_log"]:
            c1.SetLogz(1)
            obj.GetZaxis().SetMoreLogLabels(opts["zaxis_moreloglabels"])
            obj.GetZaxis().SetNoExponent(opts["zaxis_noexponents"])


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

def plot_hist_2d_projections(hist,options={}):

    c1 = r.TCanvas("c1","c1",800,800)

    style = utils.set_style_2d()
    # style.SetPadRightMargin(0.)
    # style.SetPadTopMargin(0.)

    # pad_main = r.TPad("pad1","pad1",0.20,0.20,1.0,1.0)
    # pad_bottom = r.TPad("pad2","pad2",0.0, 0.0, 1.0, 0.20)
    # pad_left = r.TPad("pad2","pad2",0.0, 0.0, 0.20, 1)

    pad_main = r.TPad("pad1","pad1",0,0,0.8,0.8)
    pad_top = r.TPad("pad2","pad2",0,0.8,0.8,1)
    pad_right = r.TPad("pad3","pad3",0.8,0,1,0.8)
    pad_corner = r.TPad("pad4","pad4",0.8,0.8,1.,1.)

    pad_main.SetRightMargin(0.01)
    pad_top.SetRightMargin(0.)
    pad_top.SetBottomMargin(0.)
    pad_main.SetTopMargin(0.01)
    pad_right.SetTopMargin(0.)
    pad_right.SetLeftMargin(0.)

    pad_top.Draw()
    pad_right.Draw()
    pad_main.Draw()
    pad_corner.Draw()


    pad_top.cd()
    projx = hist.ProjectionX()
    print projx

    projx.SetMarkerStyle(20)
    projx.SetMarkerSize(0.8)
    projx.SetLineColor(r.kBlack)
    projx.SetLineWidth(2)
    projx.SetTitle("")
    projx.GetYaxis().SetTitleOffset(0.25)
    projx.GetYaxis().SetTitleSize(0.2)
    projx.GetYaxis().SetNdivisions(405)
    projx.GetYaxis().SetLabelSize(0.13)
    projx.GetXaxis().SetLabelSize(0.)
    projx.GetXaxis().SetTickSize(0.06)

    projx.Draw("LPE")

    pad_right.cd()
    projy = hist.ProjectionY()
    print projy
    projy.SetFillStyle(0)

    projy.SetMarkerStyle(20)
    projy.SetMarkerSize(0.8)
    projy.SetLineWidth(2)
    projy.SetTitle("")
    projy.GetYaxis().SetTitleOffset(0.25)
    projy.GetYaxis().SetTitleSize(0.2)
    projy.GetYaxis().SetNdivisions(505)
    projy.GetYaxis().SetLabelSize(0.13)
    projy.GetXaxis().SetLabelSize(0.)
    projy.GetXaxis().SetTickSize(0.06)

    projy.Draw("hbarLPE")

    pad_main.cd()


    opts = Options(options, kind="2d")


    utils.set_palette(style, opts["palette_name"])


    hist.Draw(opts["draw_option_2d"])

    # pad_corner.cd()
    # hist.Draw(opts["draw_option_2d"])
    # r.gPad.Update()
    # palette = hist.GetListOfFunctions().FindObject("palette")
    # print list(hist.GetListOfFunctions())
    # # palette.SetX1NDC(0.0);
    # # palette.SetY1NDC(0.0);
    # # palette.SetX2NDC(1.0);
    # # palette.SetY2NDC(1.0);
    # palette.Draw()
    # r.gPad.Modified();
    # r.gPad.Update();
    # pad_main.cd()

    hist.SetTitle(opts["title"])

    hist.SetMarkerSize(opts["bin_text_size"])
    style.SetPaintTextFormat(opts["bin_text_format"])

    if opts["bin_text_smart"]:
        utils.draw_smart_2d_bin_labels(hist, opts)

    draw_cms_lumi(pad_main, opts)
    handle_axes(pad_main, hist, opts)
    draw_extra_stuff(pad_main, opts)
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

    if opts["extra_text"]:
        t = r.TLatex()
        t.SetTextAlign(12)
        t.SetTextFont(42)
        t.SetTextColor(r.kBlack)
        t.SetTextSize(0.04)
        for itext, text in enumerate(opts["extra_text"]):
            t.DrawLatexNDC(opts["extra_text_xpos"],0.87-itext*0.05,text)


def save(c1, opts):

    fname = opts["output_name"]
    print ">>> Saving {}".format(fname)
    c1.SaveAs(fname)
    if opts["output_ic"]:
        os.system("ic {}".format(fname))
    if opts["output_jsroot"]:
        r.TBufferJSON.ExportToFile("{}.json".format(fname.rsplit(".",1)[0]),c1)

if __name__ == "__main__":

    pass

    scalefact_all = 100
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
    hdata.FillRandom("expo",int(1*scalefact_all)) # signal injection

    hsig1 = r.TH1F("hsig1","hsig1",nbins,0,5)
    hsig1.FillRandom("expo",int(scalefact_mc*1*scalefact_all))
    hsig1.Scale(1./scalefact_mc)

    hsig2 = r.TH1F("hsig2","hsig2",nbins,0,5)
    hsig2.FillRandom("gaus",int(scalefact_mc*1*scalefact_all))
    hsig2.Scale(1./scalefact_mc)


    plot_hist(
            data=hdata,
            bgs=[h1,h2,h3],
            sigs = [hsig1, hsig2],
            sig_labels = ["SUSY", "Black hole"],
            colors = [r.kRed-2, r.kAzure+2, r.kGreen-2],
            legend_labels = ["first", "second", "third"],
            options = {
                # "draw_points": True,
                "do_stack": True,
                # "legend_alignment": "bottom left",
                "legend_smart": True,
                # "legend_alignment": "top right",
                "legend_scalex": 0.7,
                "legend_scaley": 1.5,
                # "legend_ncolumns": 2,
                "legend_opacity": 0.5,
                "extra_text": ["#slash{E}_{T} > 50 GeV","N_{jets} #geq 2","H_{T} > 300 GeV"],
                "extra_text_xpos": 0.35,
                # "yaxis_log": True,
                # "show_bkg_smooth": True,
                "yaxis_moreloglabels": True,
                "ratio_range":[0.8,1.2],
                # "ratio_numden_indices": [0,1],
                # "hist_disable_xerrors": True,
                # "ratio_chi2prob": True,
                "output_name": "test1.pdf",
                "legend_percentageinbox": True,
                "cms_label": "Preliminary",
                "lumi_value": "-inf",
                "output_ic": True,
                "us_flag": True,
                # "output_jsroot": True,
                }
            )

    # plot_hist(
    #         data=None,
    #         bgs=[h1,h2],
    #         colors = [r.kRed-2, r.kAzure+2],
    #         legend_labels = ["first", "second", "third"],
    #         options = {
    #             "do_stack": False,
    #             "legend_alignment": "bottom left",
    #             "legend_scalex": 0.9,
    #             "legend_scaley": 0.6,
    #             # "legend_ncolumns": 2,
    #             "legend_opacity": 0.5,
    #             "extra_text": ["#slash{E}_{T} > 50 GeV","N_{jets} #geq 2","H_{T} > 300 GeV"],
    #             "extra_text_xpos": 0.35,
    #             # "yaxis_log": True,
    #             # "show_bkg_smooth": True,
    #             "yaxis_moreloglabels": True,
    #             "ratio_range":[0.8,1.2],
    #             # "ratio_numden_indices": [0,1],
    #             # "hist_disable_xerrors": True,
    #             # "ratio_chi2prob": True,
    #             "output_name": "test1.pdf",
    #             "legend_percentageinbox": True,
    #             "cms_label": "Preliminary",
    #             "lumi_value": "-inf",
    #             "output_ic": True,
    #             "us_flag": True,
    #             # "output_jsroot": True,
    #             }
    #         )

