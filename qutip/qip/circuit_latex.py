# This file is part of QuTiP: Quantum Toolbox in Python.
#
#    Copyright (c) 2011 and later, Paul D. Nation and Robert J. Johansson.
#    All rights reserved.
#
#    Redistribution and use in source and binary forms, with or without
#    modification, are permitted provided that the following conditions are
#    met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#    3. Neither the name of the QuTiP: Quantum Toolbox in Python nor the names
#       of its contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#
#    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#    HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###############################################################################
import os

_latex_template = r"""
\documentclass{standalone}
%s
\begin{document}
\Qcircuit @C=1cm @R=1cm {
%s}
\end{document}
"""


def _latex_compile(code, filename="qcirc", format="png"):
    """
    Requires: pdflatex, pdfcrop, pdf2svg, imagemagick (convert)
    """
    os.system("rm -f %s.tex %s.pdf %s.png" % (filename, filename, filename))

    with open(filename + ".tex", "w") as file:
        file.write(_latex_template % (_qcircuit_latex_min, code))

    os.system("pdflatex -interaction batchmode %s.tex" % filename)
    os.system("rm -f %s.aux %s.log" % (filename, filename))
    os.system("pdfcrop %s.pdf %s-tmp.pdf" % (filename, filename))
    os.system("mv %s-tmp.pdf %s.pdf" % (filename, filename))

    if format == 'png':
        os.system("convert -density %s %s.pdf %s.png" % (100, filename,
                                                         filename))
        with open("%s.png" % filename, "rb") as f:
            result = f.read()
    else:
        os.system("pdf2svg %s.pdf %s.svg" % (filename, filename))
        with open("%s.svg" % filename) as f:
            result = f.read()

    return result


_qcircuit_latex_min = r"""
%    qcircuit version 2.6.0
%    Contributors: Steve Flammia, Bryan Eastin, Travis Scholten
%    License: http://www.gnu.org/licenses/gpl-2.0.html
%    Original file: https://github.com/CQuIC/qcircuit/blob/master/qcircuit.sty
%    Edited for QuTiP : 02/29/2020

\usepackage{xy}
\xyoption{matrix}
\xyoption{frame}
\xyoption{arrow}
\xyoption{arc}

\usepackage{ifpdf}

\DeclareOption{braket}{
    \newcommand{\bra}[1]{\ensuremath{\left\langle{#1}\right\vert}}
    \newcommand{\ket}[1]{\ensuremath{\left\vert{#1}\right\rangle}}
    }

\DeclareOption{qm}{
    \newcommand{\ip}[2]{\ensuremath{\left\langle{#1}\middle\vert{#2}\right\rangle}}
    \newcommand{\melem}[3]{\ensuremath{\left\langle{#1}\middle\vert{#2}\middle\vert{#3}\right\rangle}}
    \newcommand{\expval}[1]{\ensuremath{\left\langle #1 \right\rangle}}
    \newcommand{\op}[2]{\ensuremath{\left\vert{#1}\middle\rangle\middle\langle{#2}\right\vert}}
}

\ProcessOptions\relax

% The following resets Xy-pic matrix alignment to the pre-3.8 default, as
% required by Qcircuit.
\entrymodifiers={!C\entrybox}

\newcommand{\qw}[1][-1]{\ar @{-} [0,#1]}
    % Defines a wire that connects horizontally.  By default it connects to the object on the left of the current object.
    % WARNING: Wire commands must appear after the gate in any given entry.
\newcommand{\qwx}[1][-1]{\ar @{-} [#1,0]}
    % Defines a wire that connects vertically.  By default it connects to the object above the current object.
    % WARNING: Wire commands must appear after the gate in any given entry.
\newcommand{\qwa}[1][-1]{\ar @{<-} [0,#1]}
    % Defines a wire that connects horizontally with an arrow.  By default it makes an end wire with an arrow indicating the end of the circuit.
    % WARNING: Wire commands must appear after the gate in any given entry.
\newcommand{\cw}[1][-1]{\ar @{=} [0,#1]}
    % Defines a classical wire that connects horizontally.  By default it connects to the object on the left of the current object.
    % WARNING: Wire commands must appear after the gate in any given entry.
\newcommand{\cwx}[1][-1]{\ar @{=} [#1,0]}
    % Defines a classical wire that connects vertically.  By default it connects to the object above the current object.
    % WARNING: Wire commands must appear after the gate in any given entry.
\newcommand{\cwa}[1][-1]{\ar @{<=} [0,#1]}
    % Defines a classical wire that connects horizontally with an arrow.  By default it makes an end wire with an arrow indicating the end of the circuit.
    % WARNING: Wire commands must appear after the gate in any given entry.
\newcommand{\cds}[2]{*+<1em,.9em>{\hphantom{#2}} \POS [0,0].[#1,0]="e",!C *{#2};"e"+ R \qw}
    % Allows the insertion of text without a box and exands circuit around this text.
    % This is useful for such things as ... to indicate a generalized circuit.
\newcommand{\barrier}[2][-0.95em]{\ar @{--}[#2,1]+<#1, -1em>;[0,1]+<#1, 1em>}
    % Defines a barrier that is represented by a horizontal dashed line.
    % It takes a a single argument to specify how many bits to cover
    % To center the barrier between gates you can adjust the horizontal offset
    % with an optional second parameter. This is the horizontal offset in em.
    % It defaults to -0.95em
    % WARNING: Be sure to place the barrier on the topmost bit it covers, it only propogates downwards
\newcommand{\gate}[1]{*+<.6em>{#1} \POS ="i","i"+UR;"i"+UL **\dir{-};"i"+DL **\dir{-};"i"+DR **\dir{-};"i"+UR **\dir{-},"i" \qw}
    % Boxes the argument, making a gate.
\newcommand{\sgate}[2]{\gate{#1}  \qwx[#2]}
    % Creates a gate and a qwx wire going #2 spots below, for a gate split over
    % non-adjacent rows
\newcommand{\meter}{*=<1.8em,1.4em>{\xy ="j","j"-<.778em,.322em>;{"j"+<.778em,-.322em> \ellipse ur,_{}},"j"-<0em,.4em>;p+<.5em,.9em> **\dir{-},"j"+<2.2em,2.2em>*{},"j"-<2.2em,2.2em>*{} \endxy} \POS ="i","i"+UR;"i"+UL **\dir{-};"i"+DL **\dir{-};"i"+DR **\dir{-};"i"+UR **\dir{-},"i" \qw}
    % Inserts a measurement meter.
    % In case you're wondering, the constants .778em and .322em specify
    % one quarter of a circle with radius 1.1em.
    % The points added at + and - <2.2em,2.2em> are there to strech the
    % canvas, ensuring that the size is unaffected by erratic spacing issues
    % with the arc.
\newcommand{\metersymb}{\xy ="j","j"-<.778em,.322em>;{"j"+<.778em,-.322em> \ellipse ur,_{}},"j"-<0em,.4em>;p+<.5em,.9em> **\dir{-},"j"+<2.2em,2.2em>*{},"j"-<2.2em,2.2em>*{} \endxy}
    % A longer meter
\newcommand{\meterB}[1]{*=<1.8em,2.6em>{\xy 0;<0em,-.8em>:
0*{\begingroup
\everymath{\scriptstyle}
\tiny #1 \endgroup},<0em,.7em>*{\xy ="j","j"-<.778em,-.322em>;{"j"+<.778em,.322em> \ellipse ur,_{}},"j"-<0em,-.2em>;p+<.5em,.9em> **\dir{-},"j"+<2.2em,2.2em>*{},"j"-<2.2em,2.2em>*{} \endxy}
\endxy} \POS ="i","i"+UR;"i"+UL **\dir{-};"i"+DL **\dir{-};"i"+DR **\dir{-};"i"+UR **\dir{-},"i" \qw}
    % A meter that allows for a measurement operator to be added below
\newcommand{\smeterB}[2]{\meterB{#1} \qwx[#2] \qw}
    % A split meter that allows for a measurement operator to be split over non-
    % adjacent rows
\newcommand{\measure}[1]{*+[F-:<.9em>]{#1} \qw}
    % Inserts a measurement bubble with user defined text.
\newcommand{\measuretab}[1]{*{\xy*+<.6em>{#1}="e";"e"+UL;"e"+UR **\dir{-};"e"+DR **\dir{-};"e"+DL **\dir{-};"e"+LC-<.5em,0em> **\dir{-};"e"+UL **\dir{-} \endxy} \qw}
    % Inserts a measurement tab with user defined text.
\newcommand{\measureD}[1]{*{\xy*+=<0em,.1em>{#1}="e";"e"+UR+<0em,.25em>;"e"+UL+<-.5em,.25em> **\dir{-};"e"+DL+<-.5em,-.25em> **\dir{-};"e"+DR+<0em,-.25em> **\dir{-};{"e"+UR+<0em,.25em>\ellipse^{}};"e"+C:,+(0,1)*{} \endxy} \qw}
    % Inserts a D-shaped measurement gate with user defined text.
\newcommand{\multimeasure}[2]{*+<1em,.9em>{\hphantom{#2}} \qw \POS[0,0].[#1,0];p !C *{#2},p \drop\frm<.9em>{-}}
    % Draws a multiple qubit measurement bubble starting at the current position and spanning #1 additional gates below.
    % #2 gives the label for the gate.
    % You must use an argument of the same width as #2 in \ghost for the wires to connect properly on the lower lines.
\newcommand{\multimeasureD}[2]{*+<1em,.9em>{\hphantom{#2}} \POS [0,0]="i",[0,0].[#1,0]="e",!C *{#2},"e"+UR-<.8em,0em>;"e"+UL **\dir{-};"e"+DL **\dir{-};"e"+DR+<-.8em,0em> **\dir{-};{"e"+DR+<0em,.8em>\ellipse^{}};"e"+UR+<0em,-.8em> **\dir{-};{"e"+UR-<.8em,0em>\ellipse^{}},"i" \qw}
    % Draws a multiple qubit D-shaped measurement gate starting at the current position and spanning #1 additional gates below.
    % #2 gives the label for the gate.
    % You must use an argument of the same width as #2 in \ghost for the wires to connect properly on the lower lines.
\newcommand{\control}{*!<0em,.025em>-=-<.2em>{\bullet}}
    % Inserts an unconnected control.
\newcommand{\controlo}{*+<.01em>{\xy -<.095em>*\xycircle<.19em>{} \endxy}}
    % Inserts a unconnected control-on-0.
\newcommand{\ctrl}[1]{\control \qwx[#1] \qw}
    % Inserts a control and connects it to the object #1 wires below.
\newcommand{\ctrlo}[1]{\controlo \qwx[#1] \qw}
    % Inserts a control-on-0 and connects it to the object #1 wires below.
\newcommand{\cctrl}[1]{\control \cwx[#1] \cw}
    % Inserts a classical control and connects it to the object #1 wires below.
\newcommand{\cctrlo}[1]{\controlo \cwx[#1] \cw}
    % Inserts a classical control-on-0 and connects it to the object #1 wires below.
\newcommand{\targ}{*+<.02em,.02em>{\xy ="i","i"-<.39em,0em>;"i"+<.39em,0em> **\dir{-}, "i"-<0em,.39em>;"i"+<0em,.39em> **\dir{-},"i"*\xycircle<.4em>{} \endxy} \qw}
    % Inserts a CNOT target.
\newcommand{\qswap}{*=<0em>{\times} \qw}
    % Inserts half a swap gate.
    % Must be connected to the other swap with \qwx.
\newcommand{\multigate}[2]{*+<1em,.9em>{\hphantom{#2}} \POS [0,0]="i",[0,0].[#1,0]="e",!C *{#2},"e"+UR;"e"+UL **\dir{-};"e"+DL **\dir{-};"e"+DR **\dir{-};"e"+UR **\dir{-},"i" \qw}
    % Draws a multiple qubit gate starting at the current position and spanning #1 additional gates below.
    % #2 gives the label for the gate.
    % You must use an argument of the same width as #2 in \ghost for the wires to connect properly on the lower lines.
\newcommand{\ghost}[1]{*+<1em,.9em>{\hphantom{#1}} \qw}
    % Leaves space for \multigate on wires other than the one on which \multigate appears.  Without this command wires will cross your gate.
    % #1 should match the second argument in the corresponding \multigate.
\newcommand{\cghost}[1]{*+<1em,.9em>{\hphantom{#1}} \cw}
    % Same as ghost but with a classical incoming wire.
\newcommand{\nghost}[1]{*+<1em,.9em>{\hphantom{#1}}}
    % Same as ghost but with no incoming wire.
\newcommand{\push}[1]{*{#1}}
    % Inserts #1, overriding the default that causes entries to have zero size.  This command takes the place of a gate.
    % Like a gate, it must precede any wire commands.
    % \push is useful for forcing columns apart.
    % NOTE: It might be useful to know that a gate is about 1.3 times the height of its contents.  I.e. \gate{M} is 1.3em tall.
    % WARNING: \push must appear before any wire commands and may not appear in an entry with a gate or label.
\newcommand{\gategroup}[6]{\POS"#1,#2"."#3,#2"."#1,#4"."#3,#4"!C*+<#5>\frm{#6}}
    % Constructs a box or bracket enclosing the square block spanning rows #1-#3 and columns=#2-#4.
    % The block is given a margin #5/2, so #5 should be a valid length.
    % #6 can take the following arguments -- or . or _\} or ^\} or \{ or \} or _) or ^) or ( or ) where the first two options yield dashed and
    % dotted boxes respectively, and the last eight options yield bottom, top, left, and right braces of the curly or normal variety.  See the Xy-pic reference manual for more options.
    % \gategroup can appear at the end of any gate entry, but it's good form to pick either the last entry or one of the corner gates.
    % BUG: \gategroup uses the four corner gates to determine the size of the bounding box.  Other gates may stick out of that box.  See \prop.
\newcommand{\inputgroupv}[5]{\POS"#1,1"."#2,1"."#1,1"."#2,1"!C*+<#3>\frm{\{}, \POS"#1,1"."#2,1"."#1,1"."#2,1"*!C!<1.7em,#4>=<0em>{#5}}
    % Constructs an input group with label #5 and a grouping { from rows #1 to #2 with #3 and #4 controlling the spacing
\newcommand{\inputgroup}[4]{\POS"#1,1"."#2,1"."#1,1"."#2,1", \POS"#1,1"."#2,1"."#1,1"."#2,1"*!C!<1em,#3>=<0em>{#4}}
    % Constructs an input group with label #4 from rows #1 to #2 with #3 controlling the spacing
\newcommand{\inputgrouph}[5]{\POS"#1,1"."#2,1"."#1,1"."#2,1", \POS"#1,1"."#2,1"."#1,1"."#2,1"*!C!<#5,#3>=<0em>{#4}}
    % Constructs an input group with label #4 and a grouping /vdots from rows #1 to #2 with #3 and #5 controlling the spacing
\newcommand{\rstick}[1]{*!L!<-.5em,0em>=<0em>{#1}}
    % Centers the left side of #1 in the cell.  Intended for lining up wire labels.  Note that non-gates have default size zero.
\newcommand{\lstick}[1]{*!R!<.5em,0em>=<0em>{#1}}
    % Centers the right side of #1 in the cell.  Intended for lining up wire labels.  Note that non-gates have default size zero.
\newcommand{\ustick}[1]{*!D!<0em,-.5em>=<0em>{#1}}
    % Centers the bottom of #1 in the cell.  Intended for lining up wire labels.  Note that non-gates have default size zero.
\newcommand{\dstick}[1]{*!U!<0em,.5em>=<0em>{#1}}
    % Centers the top of #1 in the cell.  Intended for lining up wire labels.  Note that non-gates have default size zero.
\newcommand{\Qcircuit}{\xymatrix @*=<0em>}
    % Defines \Qcircuit as an \xymatrix with entries of default size 0em.
\newcommand{\link}[2]{\ar @{-} [#1,#2]}
    % Draws a wire or connecting line to the element #1 rows down and #2 columns forward.
\newcommand{\pureghost}[1]{*+<1em,.9em>{\hphantom{#1}}}
    % Same as \ghost except it omits the wire leading to the left.
"""
