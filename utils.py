import ROOT as r


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
    tdr_style.SetPadTopMargin(0.10)
    tdr_style.SetPadBottomMargin(0.15)
    tdr_style.SetPadLeftMargin(0.15)
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

    # For the axis titles:
    tdr_style.SetTitleColor(1, "XYZ")
    tdr_style.SetTitleFont(42, "XYZ")
    tdr_style.SetTitleSize(0.045, "XYZ")
    tdr_style.SetTitleOffset(1.17, "X")
    tdr_style.SetTitleOffset(1.15, "Y")

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
    def interp1d(one,two,ndiv):
        return [one+1.0*(two-one)*i/(ndiv-1) for i in range(ndiv)]
    return zip(*map(lambda x: interp1d(x[0],x[1],ndiv), zip(first,second)))

def draw_flag(c1, cx, cy, size, _persist=[]):
    c1.cd();
    aspect_ratio = c1.GetWindowWidth()/c1.GetWindowHeight();
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
