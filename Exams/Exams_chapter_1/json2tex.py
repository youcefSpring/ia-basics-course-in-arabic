import json, re, sys
src, out = sys.argv[1], sys.argv[2]
title = sys.argv[3] if len(sys.argv) > 3 else 'الواجب الأول'
subtitle = sys.argv[4] if len(sys.argv) > 4 else 'في الذكاء الاصطناعي'
d = json.load(open(src, encoding='utf-8'))

def tex(s):
    for a, b in [('\\', r'\textbackslash{}'), ('&', r'\&'), ('%', r'\%'), ('$', r'\$'),
                 ('#', r'\#'), ('_', r'\_'), ('{', r'\{'), ('}', r'\}')]:
        s = s.replace(a, b)
    s = s.replace(r'\textbackslash\{\}', r'\textbackslash{}')
    # wrap Latin runs so they render left-to-right
    s = re.sub(r'[A-Za-z][A-Za-z0-9.\- ]*[A-Za-z0-9]|[A-Za-z]',
                  lambda m: r'\textenglish{' + m.group(0) + '}', s)
    return s.replace('←', r'$\leftarrow$')

def pts(p):
    return ('%g' % p).replace('.', ',')

letters = ['أ', 'ب', 'ج', 'د', 'هـ', 'و', 'ز', 'ح']
total = sum(q['points'] for q in d['questions'])
items = []
for q in d['questions']:
    opts = []
    for i, o in enumerate(q['options']):
        mark = r'\correctbox' if o['is_correct'] else r'\emptybox'
        body = tex(o['text'])
        if o['is_correct']:
            body = r'\correct{' + body + '}'
        opts.append(r'    \item[%s\ \textbf{%s)}] %s' % (mark, letters[i], body))
    items.append('\n'.join([
        r'\needspace{9\baselineskip}\item',
        r'\textbf{%s} \hfill \pts{%s}' % (tex(q['question_text']), pts(q['points'])),
        r'\begin{itemize}[leftmargin=1.6cm, labelsep=0.3cm, itemsep=2pt, topsep=4pt]',
        *opts,
        r'\end{itemize}',
        r'\explanation{%s}' % tex(q['explanation']),
    ]))

tpl = r'''\documentclass[a4paper]{article}

%------------------------------------------------
% الحزم
%------------------------------------------------

\usepackage{enumitem}
\usepackage[margin=2.5cm]{geometry}
\usepackage{amsmath,amsfonts,amssymb}
\usepackage[charter]{mathdesign}
\usepackage{graphicx}
\usepackage{array}
\usepackage{xcolor}
\usepackage{needspace}
\usepackage{fancyhdr}
\usepackage{polyglossia}

%------------------------------------------------
% اللغات والخطوط
%------------------------------------------------

\setdefaultlanguage[
    calendar=gregorian,
    numerals=maghrib
]{arabic}

\setotherlanguage{english}

% إذا لم تكن الخطوط مثبتة في الجهاز، تُؤخذ من المجلد ../../fonts/
\IfFontExistsTF{Amiri}{%
    \newfontfamily\arabicfont[Script=Arabic, Scale=1.2]{Amiri}
}{%
    \newfontfamily\arabicfont[
        Script=Arabic, Scale=1.2,
        Path=../../fonts/, Extension=.ttf,
        UprightFont=*-Regular, BoldFont=*-Bold,
        ItalicFont=*-Italic, BoldItalicFont=*-BoldItalic
    ]{Amiri}
}

\IfFontExistsTF{AlBattar}{%
    \newfontfamily\arabicfontsf[Script=Arabic, Scale=1.3]{AlBattar}
    \newfontfamily\khatt[Script=Arabic, Scale=1.3]{AlBattar}
}{%
    \newfontfamily\arabicfontsf[
        Script=Arabic, Scale=1.3, Path=../../fonts/,
        BoldFont=ae_AlBattar.ttf
    ]{ae_AlBattar.ttf}
    \newfontfamily\khatt[
        Script=Arabic, Scale=1.3, Path=../../fonts/,
        BoldFont=ae_AlBattar.ttf
    ]{ae_AlBattar.ttf}
}

%------------------------------------------------
% نسخة الطالب / نسخة التصحيح
% لإنتاج نسخة التصحيح: عرّف \withanswers قبل \input لهذا الملف
%------------------------------------------------

\newif\ifcorrection
\ifdefined\withanswers \correctiontrue \else \correctionfalse \fi

\newcommand{\emptybox}{$\square$}
\ifcorrection
    \newcommand{\correctbox}{\textcolor{green!50!black}{$\boxtimes$}}
    \newcommand{\correct}[1]{\textcolor{green!40!black}{\textbf{#1}}}
    \newcommand{\explanation}[1]{%
        \par\vspace{3pt}
        \fcolorbox{gray!60}{gray!8}{\parbox{\dimexpr\linewidth-2\fboxsep-2\fboxrule}{%
        \small\textbf{التعليل:} #1}}}
\else
    \newcommand{\correctbox}{$\square$}
    \newcommand{\correct}[1]{#1}
    \newcommand{\explanation}[1]{}
\fi

\newcommand{\pts}[1]{\textbf{(#1 ن)}}

%------------------------------------------------
% إعداد الصفحة
%------------------------------------------------

\renewcommand{\footrulewidth}{1pt}
\renewcommand{\headrulewidth}{1pt}

\rhead{\khatt المدرسة العليا للأساتذة ببوزريعة}
\lhead{\khatt ملحقة بومرداس}

\cfoot{\thepage}
\lfoot{\khatt الأستاذ: د. بن عبد الرزاق يوسف}

\parindent 0pt
\setlength{\headsep}{15pt}
\arraycolsep=1.4pt

\pagestyle{fancy}

\setlist[enumerate,1]{label=\textbf{السؤال \arabic*:}, leftmargin=*, itemsep=12pt, align=left}

%================================================
% بداية الوثيقة
%================================================

\begin{document}

\begin{center}

{\Large\khatt\textbf{__TITLE__}\ifcorrection\ \textbf{-- التصحيح النموذجي}\fi}

\vspace{0.2cm}

{\Large\khatt\textbf{__SUBTITLE__}}

\end{center}

\rule{\textwidth}{1pt}

\ifcorrection\else
\textbf{الاسم واللقب:} \dotfill \quad \textbf{الفوج:} \makebox[3cm]{\dotfill}

\vspace{0.3cm}
\fi

\begin{center}

{\khatt\textbf{أسئلة متعددة الاختيارات (__N__ سؤالا -- __TOTAL__ نقطة)}}

\end{center}

\rule{\textwidth}{1pt}

\textbf{التعليمة:} ضع علامة \textbf{$\times$} في المربع المقابل للإجابة الصحيحة. لكل سؤال إجابة صحيحة واحدة فقط.

\vspace{0.3cm}

\begin{enumerate}

__ITEMS__

\end{enumerate}

\vfill
\begin{center}
{\khatt بالتوفيق}
\end{center}

\end{document}
'''
tpl = (tpl.replace('__TITLE__', title).replace('__SUBTITLE__', subtitle).replace('__N__', str(len(d['questions'])))
          .replace('__TOTAL__', pts(total))
          .replace('__ITEMS__', '\n\n%------------------------------------------------\n\n'.join(items)))
open(out, 'w', encoding='utf-8').write(tpl)
