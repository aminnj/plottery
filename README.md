# plottery
## Introduction
A ROOT plotter that makes you feel like a millionaire ("lottery", get it?). Some interesting features include
* Percentages in marker boxes in the legend
* Automatic legend placement to prevent overlaps
* A US flag stamp
* Chi2 probability calculation for ratio pads
* Automatic range for ratio pad
* Pull distribution markers have numbers representing n-sigma, and have mean/standard deviation shown

...and it supports
* TH1
* TGraph(AsymmErrors)
* TH2

A list of options is shown below, and there is a "self-documenting" class containing all of them in the source.

## Instructions
* You need ROOT
* Modify and execute `examples.py` to see some examples (which get put into `examples/`)

## Design philosophies
* Generally, plotting scripts grow endlessly to encompass use-cases that crop up over the years.
In principle, plottery should comfortably handle 95% of use-cases to prevent the size from blowing up.
* Plottery is only a plotter. It is not a histogram-adder, a re-binner, a TTree looper, etc.
Features like that should be written around plottery, not within it.
* Options should be functionally grouped (e.g., options applying to legend should start with `legend_`, options
applying to the x-axis should start with `xaxis_`). See the list of supported options below for an idea. Also, this
makes it so printing out options alphabetically retains a logical grouping.

## List of supported options
Note that the following list was obtained _verbatim_ with
```bash
python -c "__import__('plottery').Options().usage()"
```
* `bin_text_format` [String]
    format string for text in TH2 bins (default: ".1f")
* `bin_text_format_smart` [String]
    python-syntax format string for smart text in TH2 bins taking value and bin error (default: "{0:.0f}#pm{1:.0f}")
* `bin_text_size` [Float]
    size of text in bins (TH2::SetMarkerSize) (default: 1.7)
* `bin_text_smart` [Boolean]
    change bin text color for aesthetics (default: False)
* `bkg_sort_method` [Boolean]
    how to sort background stack using integrals: 'unsorted', 'ascending', or 'descending' (default: "ascending")
* `cms_label` [String]
    E.g., 'Preliminary'; default hides label (default: None)
* `do_stack` [Boolean]
    stack histograms (default: True)
* `draw_option_2d` [String]
    hist draw option (default: "colz")
* `draw_points` [Boolean]
    draw points instead of fill (default: False)
* `extra_text` [List]
    list of strings for textboxes (default: [])
* `extra_text_xpos` [Float]
    NDC x position (0 to 1) for extra text (default: 0.3)
* `hist_disable_xerrors` [Boolean]
    Disable the x-error bars on data for 1D hists (default: True)
* `hist_line_black` [Boolean]
    Black lines for histograms (default: False)
* `hist_line_none` [Boolean]
    No lines for histograms, only fill (default: False)
* `legend_alignment` [Boolean]
    easy alignment of TLegend. String containing two words from: bottom, top, left, right (default: "")
* `legend_border` [Boolean]
    show legend border? (default: True)
* `legend_coordinates` [List]
    4 elements specifying TLegend constructor coordinates (default: [0.63, 0.67, 0.93, 0.87])
* `legend_ncolumns` [Int]
    number of columns in the legend (default: 1)
* `legend_opacity` [Float]
    from 0 to 1 representing the opacity of the TLegend white background (default: 0.5)
* `legend_percentageinbox` [Boolean]
    show relative process contributions as %age in the legend thumbnails (default: True)
* `legend_scalex` [Float]
    scale width of legend by this factor (default: 1)
* `legend_scaley` [Float]
    scale height of legend by this factor (default: 1)
* `legend_smart` [Boolean]
    Smart alignment of legend to prevent overlaps (default: True)
* `lumi_unit` [String]
    Unit for lumi label (default: "fb")
* `lumi_value` [String]
    E.g., 35.9; default hides lumi label (default: "")
* `output_ic` [Boolean]
    run `ic` (imgcat) on output (default: False)
* `output_jsroot` [Boolean]
    output .json for jsroot (default: False)
* `output_name` [String]
    output file name/path (default: "plot.pdf")
* `palette_name` [String]
    color palette: 'default', 'rainbow', 'susy', etc. (default: "default")
* `ratio_chi2prob` [Boolean]
    show chi2 probability for ratio (default: False)
* `ratio_horizontal_lines` [List]
    list of y-values to draw horizontal line (default: [1.0])
* `ratio_name` [String]
    name of ratio pad (default: "Data/MC")
* `ratio_ndivisions` [Int]
    SetNdivisions integer for ratio (default: 505)
* `ratio_numden_indices` [List]
    Pair of numerator and denominator histogram indices (from `bgs`) for ratio (default: None)
* `ratio_pull` [Boolean]
    show pulls instead of ratios in ratio pad (default: False)
* `ratio_pull_numbers` [Boolean]
    show numbers for pulls, and mean/sigma (default: True)
* `ratio_range` [List]
    pair for min and max y-value for ratio; default auto re-sizes to 3 sigma range (default: [-1, -1])
* `show_bkg_errors` [Boolean]
    show error bar for background stack (default: False)
* `show_bkg_smooth` [Boolean]
    show smoothed background stack (default: False)
* `title` [String]
    plot title (default: "")
* `us_flag` [Boolean]
    show the US flag in the corner (default: False)
* `us_flag_coordinates` [List]
    Specify flag location with (x pos, y pos, size) (default: [0.68, 0.96, 0.06])
* `xaxis_label` [String]
    label for x axis (default: "")
* `xaxis_log` [Boolean]
    log scale x-axis (default: False)
* `xaxis_moreloglabels` [Boolean]
    show denser labels with logscale for x axis (default: True)
* `xaxis_noexponents` [Boolean]
    don't show exponents in logscale labels for x axis (default: False)
* `xaxis_range` [List]
    2 elements to specify x axis range (default: [])
* `yaxis_label` [String]
    label for y axis (default: "Events")
* `yaxis_log` [Boolean]
    log scale y-axis (default: False)
* `yaxis_moreloglabels` [Boolean]
    show denser labels with logscale for y axis (default: True)
* `yaxis_noexponents` [Boolean]
    don't show exponents in logscale labels for y axis (default: False)
* `yaxis_range` [List]
    2 elements to specify y axis range (default: [])
* `zaxis_label` [String]
    label for z axis (default: "")
* `zaxis_log` [Boolean]
    log scale z-axis (default: False)
* `zaxis_moreloglabels` [Boolean]
    show denser labels with logscale for z axis (default: True)
* `zaxis_noexponents` [Boolean]
    don't show exponents in logscale labels for z axis (default: False)
* `zaxis_range` [List]
    2 elements to specify z axis range (default: [])
