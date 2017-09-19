import ROOT as r
from math import log


def set_style():

    tdr_style = r.TStyle("tdr_style","Style for P-TDR")

    #  For the canvas:
    tdr_style.SetCanvasBorderMode(0)
    tdr_style.SetCanvasColor(r.kWhite)
    tdr_style.SetCanvasDefH(550) # Height of canvas
    tdr_style.SetCanvasDefW(600) # Width of canvas
    tdr_style.SetCanvasDefX(0)   # Position on screen
    tdr_style.SetCanvasDefY(0)

    #  For the Pad:
    tdr_style.SetPadBorderMode(0)
    tdr_style.SetPadColor(r.kWhite)
    tdr_style.SetPadGridX(False)
    tdr_style.SetPadGridY(False)
    tdr_style.SetGridColor(0)
    tdr_style.SetGridStyle(3)
    tdr_style.SetGridWidth(1)

    #  For the frame:
    tdr_style.SetFrameBorderMode(0)
    tdr_style.SetFrameBorderSize(1)
    tdr_style.SetFrameFillColor(0)
    tdr_style.SetFrameFillStyle(0)
    tdr_style.SetFrameLineColor(1)
    tdr_style.SetFrameLineStyle(1)
    tdr_style.SetFrameLineWidth(1)

    # For the histo:
    tdr_style.SetHistLineColor(r.kBlack)
    tdr_style.SetHistLineWidth(2)
    tdr_style.SetEndErrorSize(2)
    tdr_style.SetMarkerStyle(20)

    # For the fit/function:
    tdr_style.SetOptFit(1)
    tdr_style.SetFitFormat("5.4g")
    tdr_style.SetFuncColor(2)
    tdr_style.SetFuncStyle(1)
    tdr_style.SetFuncWidth(1)

    # For the date:
    tdr_style.SetOptDate(0)

    # For the statistics box:
    tdr_style.SetOptFile(0)
    tdr_style.SetOptStat(0) #  To display the mean and RMS:   SetOptStat("mr")
    tdr_style.SetOptFit(0) #  To display the mean and RMS:   SetOptStat("mr")
    tdr_style.SetStatColor(r.kWhite)
    tdr_style.SetStatFont(42)
    tdr_style.SetStatFontSize(0.025)
    tdr_style.SetStatTextColor(1)
    tdr_style.SetStatFormat("6.4g")
    tdr_style.SetStatBorderSize(1)
    tdr_style.SetStatH(0.1)
    tdr_style.SetStatW(0.15)

    # Margins:
    tdr_style.SetPadTopMargin(0.08)
    tdr_style.SetPadBottomMargin(0.12)
    tdr_style.SetPadLeftMargin(0.13)
    tdr_style.SetPadRightMargin(0.04)

    # For the Global title:
    tdr_style.SetOptTitle(1)
    tdr_style.SetTitleFont(42)
    tdr_style.SetTitleColor(1)
    tdr_style.SetTitleTextColor(1)
    tdr_style.SetTitleFillColor(10)
    tdr_style.SetTitleFontSize(0.05)
    tdr_style.SetTitleX(0.5) #  Set the position of the title box
    tdr_style.SetTitleY(0.985) #  Set the position of the title box
    tdr_style.SetTitleAlign(23)
    tdr_style.SetTitleStyle(0)
    tdr_style.SetTitleBorderSize(0)
    tdr_style.SetTitleFillColor(0)

    r.TGaxis.SetExponentOffset(-0.06, 0, "y")
    r.TGaxis.SetExponentOffset(-0.86, -0.08, "x")

    # For the axis titles:
    tdr_style.SetTitleColor(1, "XYZ")
    tdr_style.SetTitleFont(42, "XYZ")
    tdr_style.SetTitleSize(0.045, "XYZ")
    tdr_style.SetTitleOffset(1.02, "X")
    tdr_style.SetTitleOffset(1.26, "Y")

    # For the axis labels:
    tdr_style.SetLabelColor(1, "XYZ")
    tdr_style.SetLabelFont(42, "XYZ")
    tdr_style.SetLabelOffset(0.007, "XYZ")
    tdr_style.SetLabelSize(0.040, "XYZ")

    # For the axis:
    tdr_style.SetAxisColor(1, "XYZ")
    tdr_style.SetStripDecimals(True)
    tdr_style.SetTickLength(0.03, "XYZ")
    tdr_style.SetNdivisions(510, "XYZ")
    tdr_style.SetPadTickX(1)  #  To get tick marks on the opposite side of the frame
    tdr_style.SetPadTickY(1)

    # Change for log plots:
    tdr_style.SetOptLogx(0)
    tdr_style.SetOptLogy(0)
    tdr_style.SetOptLogz(0)

    # Postscript options:
    tdr_style.SetPaperSize(20.,20.)
    tdr_style.cd()
    
    return tdr_style

def set_style_2d():
    style = set_style()
    style.SetPadBottomMargin(0.12)
    style.SetPadRightMargin(0.12)
    style.SetPadLeftMargin(0.10)
    style.SetTitleAlign(23)
    style.cd()

    return style

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

def get_default_colors():
    return [r.kSpring-6, r.kAzure+7, r.kRed-6, r.kOrange-2, r.kCyan-7, r.kMagenta-7, r.kTeal+6, r.kGray+2]


def hsv_to_rgb(h, s, v, scale=255.):
    """
    Takes hue, saturation, value 3-tuple
    and returns rgb 3-tuple
    """
    if s == 0.0: v*=scale; return [v, v, v]
    i = int(h*6.)
    f = 1.0*(h*6.)-i; p,q,t = int(scale*(v*(1.-s))), int(scale*(v*(1.-s*f))), int(scale*(v*(1.-s*(1.-f)))); v*=scale; i%=6
    if i == 0: return [v, t, p]
    if i == 1: return [q, v, p]
    if i == 2: return [p, v, t]
    if i == 3: return [p, q, v]
    if i == 4: return [t, p, v]
    if i == 5: return [v, p, q]

def rgb_to_hsv(r,g,b):
    """
    Reverse of hsv to rgb, but I think this is buggy.
    Check before using (i.e., rgb_to_hsv(hsv_to_rgb(x)) == x)
    """
    vmin = min(min(r,g),b)
    vmax = max(max(r,g),b)
    delta = 1.0*(vmax-vmin)
    value = 1.0*vmax
    if vmax > 0.:
        satur = delta/vmax
    else:
        satur = 0
        hue = -1
        return (hue,satur,value)
    if r == vmax:
        hue = 1.0*(g-b)/delta
    elif g == vmax:
        hue = 2.0+(b-r)/delta
    else:
        hue = 4.0+(r-g)/delta
    hue *= 60
    if (hue < 0): hue += 360
    return (hue,satur,value)

def interpolate_tuples(first, second, ndiv):
    """
    Given two n-tuples, and a number of divisions (ndiv), create
    ndiv n-tuples that are linearly spaced between first and second
    """
    def interp1d(one,two,ndiv):
        return [one+1.0*(two-one)*i/(ndiv-1) for i in range(ndiv)]
    return zip(*map(lambda x: interp1d(x[0],x[1],ndiv), zip(first,second)))

def get_legend_marker_info(legend):
    ncols = legend.GetNColumns()
    nrows = legend.GetNRows()
    x1 = legend.GetX1()
    y1 = legend.GetY1()
    x2 = legend.GetX2()
    y2 = legend.GetY2()
    margin = legend.GetMargin()*( x2-x1 )/ncols
    boxwidth = margin
    boxw = boxwidth*0.35
    yspace = (y2-y1)/nrows;
    coordsNDC = [] 
    for ientry in range(nrows*ncols):
        icol = ientry // nrows
        irow_in_column = ientry % nrows
        coordsNDC.append([x1+0.5*margin+((x2-x1)/ncols-(boxwidth*0.65))*icol,y2-0.5*yspace-irow_in_column*yspace])
    return { "coords": coordsNDC, "label_height": (0.6-0.1*ncols)*yspace, "box_width": boxw }

def get_stack_maximum(data, stack):
    scalefact = 1.2
    if data:
        return scalefact*max(data.GetMaximum(),stack.GetMaximum())
    else:
        return scalefact*stack.GetMaximum()

def compute_darkness(r,g,b):
    """
    Compute darkness := 1 - luminance, given RGB
    """
    return 1.0 - (0.299*r + 0.587*g + 0.114*b)

def interpolate_colors_rgb(first, second, ndiv, _persist=[]):
    """
    Create ndiv colors that are linearly interpolated between rgb triplets
    first and second
    """
    colorcodes = []
    for rgb in interpolate_tuples(first,second,ndiv):
        index = r.TColor.GetFreeColorIndex()
        _persist.append(r.TColor(index, *rgb))
        colorcodes.append(index)
    return colorcodes


def draw_flag(c1, cx, cy, size, _persist=[]):
    """
    Draw US flag
    """
    c1.cd();
    aspect_ratio = 1.33 # c1.GetWindowWidth()/c1.GetWindowHeight();
    xmin = cx-size/2.;
    xmax = cx+size/2.;
    ymin = cy-size/(2./aspect_ratio);
    ymax = cy+size/(2./aspect_ratio);
    fp = r.TPad("fp","fp",xmin,ymin,xmax,ymax);
    fp.SetFillStyle(0);
    fp.Draw();
    fp.cd();
    _persist.append(fp)
    A = 1.;
    B = 1.9;
    D = 0.76;
    G = 0.063/B;
    H = 0.063/B;
    E = 0.054;
    F = 0.054;
    for i in range(13):
        xlow = 0.;
        xhigh = 1.;
        ylow = 0.5*(1.-A/B) + i*(A/B)/13.;
        yhigh = 0.5*(1.-A/B) + (i+1)*(A/B)/13.;
        if (i >= 6): xlow = D/B;
        col = r.kWhite if i%2 else r.kRed-7
        box = r.TBox(xlow,ylow,xhigh,yhigh);
        box.SetFillColor(col);
        box.SetLineColor(col);
        box.Draw();
        _persist.append(box)

    starbox = r.TBox( 0., 0.5*(1-A/B)+6./13*(A/B), D/B, 1.-0.5*(1-A/B) );
    starbox.SetFillColor(r.kBlue-7);
    starbox.SetLineColor(r.kBlue-7);
    starbox.Draw();
    _persist.append(starbox)

    row = 0;
    inrow = 0;
    ybottom = 0.5*(1-A/B)+6./13*(1-A/B);
    starsize = 0.05+(xmax-xmin)*2.0;

    for i in range(50):

        x = -1.;
        y = -1.;
        if (inrow == 0): x = G;
        else: x = G+2*H*inrow;
        if (row == 0): y = ybottom+E;
        else: y = ybottom+E+(F*row)*(A/B);
        if (row%2!=0): x += H;

        tm = r.TMarker(x,y,r.kFullStar);
        tm.SetMarkerColor(r.kWhite);
        tm.SetMarkerSize(-1.0*starsize); # negative to flip so points upwards
        tm.Draw();
        _persist.append(tm)

        inrow += 1
        if (row%2 == 0):
            if (inrow == 6):
                inrow = 0;
                row += 1;
        else:
            if (inrow == 5):
                inrow = 0;
                row += 1;

    lab = r.TLatex(0.5,0.15,"#font[52]{Mostly made in USA}");
    lab.SetTextAlign(22);
    lab.SetTextSize(0.1);
    lab.SetTextColor(r.kGray+2);
    lab.Draw();
    _persist.append(lab)

    c1.cd();

def draw_smart_2d_bin_labels(hist,opts):
    """
    Replicate the TEXT draw option for TH2 with TLatex drawn everywhere
    but calculate the background color of each bin and draw text as 
    white or black depending on the darkness
    """
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
        darkness = compute_darkness(red, green, blue)
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

def smart_legend(legend, bgs, data=None, ymin=0., ymax=None, Nx=25, Ny=25, niters=5):
    """
    Given a TLegend, backgrounds, and optionally data,
    find a location where the TLegend doesn't overlap these objects
    preserving the width and height of the TLegend object
    by scanning over a Nx x Ny grid. If a non-overlapping position is not
    found, we decrease the legend width and height and try scanning again.
    Repeat this `niters` times before giving up.
    """

    def bar_in_box((x1,y1), (bx1,bx2,by1,by2)):
        # return true if any part of bar (top of bar represented by (x1,y1))
        # overlaps with box (bx1,bx2,by1,by2)
        does_y_overlap = by1 <= y1 <= by2
        if does_y_overlap: return x1 > bx1
        else: return False

    def point_in_box((x1,y1), (bx1,bx2,by1,by2)):
        # return true if point is in box
        return (by1 <= y1 <= by2) or (bx1 <= x1 <= bx2)

    def is_good_legend(coords, pseudo_coord):
        # return true if this pseudolegend (given by 4-tuple pseudo_coord)
        # is a good legend (i.e., doesn't overlap with list of pairs in coords
        for coord in coords:
            if bar_in_box(coord, pseudo_coord): return False
        return True

    def distance_from_corner(pseudo_coord):
        # return euclidean distance of corner of pseudo legend cloest to plot
        # pane corner (note, this is rough)
        x1,x2,y1,y2 = pseudo_coord 
        dist = 0.
        if 0.5*(y1+y2) > 0.5: dist += (1.0-y2)**2.
        else: dist += (y1)**2.
        if 0.5*(x1+x2) > 0.5: dist += (1.0-x2)**2.
        else: dist += (x1)**2.
        return dist**0.5


    allbgs = bgs[0].Clone("allbgs")
    allbgs.Reset()
    for hist in bgs:
        allbgs.Add(hist)

    if not ymax:
        ymax = allbgs.GetMaximum()

    # get coordinates of legend corners
    leg_x1 = legend.GetX1()
    leg_x2 = legend.GetX2()
    leg_y1 = legend.GetY1()
    leg_y2 = legend.GetY2()
    legend_coords = (leg_x1,leg_x2,leg_y1,leg_y2)
    legend_width, legend_height = leg_x2 - leg_x1, leg_y2 - leg_y1
    xmin = allbgs.GetBinCenter(1)
    xmax = allbgs.GetBinCenter(allbgs.GetNbinsX())
    coords = []

    # get coordinates of objects we don't want to overlap
    for ibin in range(1,allbgs.GetNbinsX()+1):
        xval = allbgs.GetBinCenter(ibin)
        yval = allbgs.GetBinContent(ibin)
        # if we have data, and it's higher than bgs, then use that value
        if data and data.GetBinContent(ibin) > yval:
                xval = data.GetBinCenter(ibin)
                yval = data.GetBinContent(ibin)
        yfrac = (yval - ymin) / (ymax - ymin)
        xfrac = (xval - xmin) / (xmax - xmin) 
        # convert from 0..1 inside plotting pane, to pad coordinates (stupid margins)
        xcoord = xfrac * (1. - r.gPad.GetLeftMargin() - r.gPad.GetRightMargin()) + r.gPad.GetLeftMargin()
        ycoord = yfrac * (1. - r.gPad.GetTopMargin() - r.gPad.GetBottomMargin()) + r.gPad.GetBottomMargin()
        coord = (xcoord, ycoord)
        coords.append(coord)

    # # draw x's to debug
    # t = r.TLatex()
    # t.SetTextAlign(22)
    # t.SetTextFont(42)
    # t.SetTextColor(r.kRed)
    # t.SetTextSize(0.03)
    # for coord in coords:
    #     t.DrawLatexNDC(coord[0],coord[1],"x")

    # generate list of legend coordinate candidates, preserving original width, height
    # move around the original legend by Nx increments in x and Ny in y
    # if we don't find anything, decrease the size and try again
    paddingx = 0.03
    paddingy = 0.03
    for iiter in range(niters):
        pseudo_coords = []
        for ix in range(Nx):
            pseudox1 = 1.0*ix/Nx + paddingx + r.gPad.GetLeftMargin()
            if pseudox1 > 1.-r.gPad.GetRightMargin()-paddingx: continue
            pseudox2 = pseudox1 + legend_width
            if pseudox2 > 1.-r.gPad.GetRightMargin()-paddingx: continue
            for iy in range(Ny):
                pseudoy1 = 1.0*iy/Ny + paddingy + r.gPad.GetBottomMargin()
                if pseudoy1 > 1.-r.gPad.GetTopMargin()-paddingy: continue
                pseudoy2 = pseudoy1 + legend_height
                if pseudoy2 > 1.-r.gPad.GetTopMargin()-paddingy: continue
                pseudo_coords.append([pseudox1,pseudox2,pseudoy1,pseudoy2])

        good_pseudo_coords = []
        for pseudo_coord in pseudo_coords:
            if not is_good_legend(coords, pseudo_coord): continue
            good_pseudo_coords.append(pseudo_coord)
        good_pseudo_coords = sorted(good_pseudo_coords, key=lambda x: distance_from_corner(x))
        if len(good_pseudo_coords) > 0:
            legend.SetX1(good_pseudo_coords[0][0])
            legend.SetX2(good_pseudo_coords[0][1])
            legend.SetY1(good_pseudo_coords[0][2])
            legend.SetY2(good_pseudo_coords[0][3])
            break
        else:
            print ">>> Running another smart legend iteration decreasing legend height and width"
            legend_width *= 0.85
            legend_height *= 0.8
    else:
        print ">>> Tried to reduce legend width, height {} times, but still couldn't find a good position!".format(niters)


