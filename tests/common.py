"""الدوال والتنسيق المشترك بين الفروض (make_tests.py) والاختبار (make_exam.py)."""
import re

LETTERS = ['أ', 'ب', 'ج', 'د', 'هـ']

# ---------- LaTeX ----------
def tex(s):
    for a, b in [('\\', '\x00'), ('&', r'\&'), ('%', r'\%'), ('$', r'\$'),
                 ('#', r'\#'), ('_', r'\_'), ('{', r'\{'), ('}', r'\}')]:
        s = s.replace(a, b)
    s = s.replace('\x00', r'\textbackslash{}')
    s = re.sub(r'[A-Za-z][A-Za-z0-9.\- ]*[A-Za-z0-9]|[A-Za-z]',
               lambda m: r'\textenglish{' + m.group(0) + '}', s)
    return s.replace('←', r'$\leftarrow$')

PREAMBLE = r'''\documentclass[11pt,a4paper]{article}
\usepackage[top=1.6cm,bottom=1.4cm,left=1.3cm,right=1.3cm,headsep=8pt,footskip=16pt]{geometry}
\usepackage{enumitem}
\usepackage{amssymb}
\usepackage{array}
\usepackage[table]{xcolor}
\usepackage{fancyhdr}
\usepackage{multicol}
\usepackage{polyglossia}
\setdefaultlanguage[calendar=gregorian, numerals=maghrib]{arabic}
\setotherlanguage{english}
\IfFontExistsTF{Amiri}{%
  \newfontfamily\arabicfont[Script=Arabic, Scale=1.08]{Amiri}
}{%
  \newfontfamily\arabicfont[Script=Arabic, Scale=1.08, Path=../fonts/, Extension=.ttf,
    UprightFont=*-Regular, BoldFont=*-Bold, ItalicFont=*-Italic,
    BoldItalicFont=*-BoldItalic]{Amiri}
}
\IfFontExistsTF{AlBattar}{%
  \newfontfamily\khatt[Script=Arabic, Scale=1.15]{AlBattar}
}{%
  \newfontfamily\khatt[Script=Arabic, Scale=1.15, Path=../fonts/,
    BoldFont=ae_AlBattar.ttf]{ae_AlBattar.ttf}
}
\renewcommand{\headrulewidth}{0.8pt}
\renewcommand{\footrulewidth}{0.8pt}
\fancyhf{}
\rhead{\khatt المدرسة العليا للأساتذة ببوزريعة}
\lhead{\khatt ملحقة بومرداس}
\lfoot{\khatt الأستاذ: د. بن عبد الرزاق يوسف}
\cfoot{\thepage/@PAGES@}
\pagestyle{fancy}
\parindent 0pt
\setlength{\columnsep}{0.6cm}
\setlength{\columnseprule}{0.4pt}
\setlist[enumerate,1]{label=\textbf{\arabic*.}, leftmargin=*, itemsep=5pt, topsep=2pt}
\begin{document}
'''


# ألوان خلفية مختلفة لصفوف جداول مفاتيح الإجابات
ROW_COLORS = ['red!14', 'orange!18', 'yellow!25', 'lime!22', 'green!16', 'teal!16',
              'cyan!16', 'blue!12', 'violet!14', 'purple!14', 'magenta!14', 'brown!18',
              'gray!18', 'olive!18']
