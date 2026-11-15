"""يولّد 12 اختبارًا (15 سؤالًا لكل منها) من بنك الأسئلة questions.py، ومفتاح الإجابات.

التوزيع في كل اختبار: 3 أسئلة سهلة، 7 متوسطة، 5 صعبة، من الفصول 1 إلى 6.
كل سؤال من البنك (180 سؤالًا) يُستعمل مرة واحدة فقط في مجموع الاختبارات.
الاستعمال:  python3 make_tests.py   ثم   tectonic test_XX.tex
"""
import random, re, sys, os
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from questions import Q

N_TESTS = 12
LETTERS = ['أ', 'ب', 'ج', 'د', 'هـ']
ORD = ['الأول', 'الثاني', 'الثالث', 'الرابع', 'الخامس', 'السادس', 'السابع',
       'الثامن', 'التاسع', 'العاشر', 'الحادي عشر', 'الثاني عشر']

# ---------- التحقق من البنك ----------
pool = defaultdict(list)
for ch, lv, stem, opts in Q:
    assert len(opts) == 5 and len(set(opts)) == 5, stem
    pool[(ch, lv)].append((ch, lv, stem, opts))
for ch in range(1, 7):
    assert [len(pool[(ch, l)]) for l in 'EMH'] == [6, 14, 10], ch

# ---------- توزيع الأسئلة على الاختبارات ----------
rng = random.Random(2026)
for k in pool:
    rng.shuffle(pool[k])
tests = []
for t in range(N_TESTS):
    easy_ch = [1, 3, 5] if t % 2 == 0 else [2, 4, 6]          # كل فصل في 6 اختبارات
    med_ch = [1, 2, 3, 4, 5, 6, t % 6 + 1]                     # كل فصل 14 مرة
    hard_ch = [c for c in range(1, 7) if c != t % 6 + 1]       # كل فصل 10 مرات
    qs = [pool[(c, 'E')].pop() for c in easy_ch]
    qs += [pool[(c, 'M')].pop() for c in sorted(med_ch)]
    qs += [pool[(c, 'H')].pop() for c in hard_ch]
    # مواضع الإجابات الصحيحة: كل حرف 3 مرات في كل اختبار
    pos = [0, 1, 2, 3, 4] * 3
    rng.shuffle(pos)
    items = []
    for (ch, lv, stem, opts), p in zip(qs, pos):
        wrong = opts[1:]
        rng.shuffle(wrong)
        items.append(dict(ch=ch, lv=lv, stem=stem,
                          opts=wrong[:p] + [opts[0]] + wrong[p:], key=p))
    tests.append(items)
assert all(not v for v in pool.values())

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
\usepackage{xcolor}
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
\cfoot{\thepage/2}
\pagestyle{fancy}
\parindent 0pt
\setlength{\columnsep}{0.6cm}
\setlength{\columnseprule}{0.4pt}
\setlist[enumerate,1]{label=\textbf{\arabic*.}, leftmargin=*, itemsep=5pt, topsep=2pt}
\begin{document}
'''

def test_tex(n, items):
    out = [PREAMBLE, r'''\begin{center}
{\Large\khatt\textbf{الاختبار %s في الذكاء الاصطناعي}}\\[2pt]
{\normalsize أسئلة متعددة الاختيارات ــ الفصول من 1 إلى 6 ــ 15 سؤالًا}
\end{center}
\vspace{-4pt}\rule{\textwidth}{0.6pt}\\
{\small\textbf{التعليمة:} لكل سؤال إجابة صحيحة واحدة فقط من بين خمسة اختيارات.
اكتب \textbf{حرف} الإجابة الصحيحة في جدول الإجابات أسفل الصفحة الثانية.
لكل سؤال نقطة واحدة (المجموع 15 نقطة).}
\vspace{-2pt}
\begin{multicols}{2}
''' % ORD[n - 1]]
    names = {'E': 'سهل', 'M': 'متوسط', 'H': 'صعب'}
    for it in items:
        out.append(r'\noindent\begin{minipage}{\linewidth}')
        out.append(r'\hangindent=0.7cm\hangafter=1\makebox[0.7cm][r]{\textbf{%d.}}\textbf{%s}' % (
            items.index(it) + 1, tex(it['stem'])))
        out.append(r'\begin{itemize}[leftmargin=0.95cm, labelsep=4pt, itemsep=0pt, topsep=2pt, parsep=0pt]')
        for i, o in enumerate(it['opts']):
            out.append(r'  \item[\textbf{%s)}] %s' % (LETTERS[i], tex(o)))
        out.append(r'\end{itemize}')
        out.append(r'\end{minipage}\par\vspace{7pt plus 4pt}')
    nums = ' & '.join(r'\textbf{%d}' % i for i in range(1, 16))
    blanks = ' & '.join([''] * 15)
    out.append(r'''\end{multicols}
\vfill
\begin{center}
{\khatt\textbf{جدول الإجابات}}\\[3pt]
\renewcommand{\arraystretch}{1.6}
\begin{tabular}{|>{\centering\arraybackslash}m{1.9cm}|*{15}{>{\centering\arraybackslash}m{0.62cm}|}}
\hline
\textbf{رقم السؤال} & %s \\ \hline
\textbf{الإجابة} & %s \\[8pt] \hline
\end{tabular}

\vspace{8pt}
\renewcommand{\arraystretch}{2.2}
\begin{tabular}{|>{\centering\arraybackslash}m{7.5cm}|>{\centering\arraybackslash}m{3.2cm}|>{\centering\arraybackslash}m{3.2cm}|}
\hline
\textbf{الاسم واللقب} & \textbf{الفوج} & \textbf{العلامة} \\ \hline
 & & \hfill /15 \\ \hline
\end{tabular}
\end{center}
\end{document}
''' % (nums, blanks))
    return '\n'.join(out)

here = os.path.dirname(os.path.abspath(__file__))
for n, items in enumerate(tests, 1):
    with open(os.path.join(here, 'test_%02d.tex' % n), 'w', encoding='utf-8') as f:
        f.write(test_tex(n, items))

# ---------- مفتاح الإجابات ----------
nums = ' & '.join(r'\textbf{%d}' % i for i in range(1, 16))
rows = '\n'.join(r'\textbf{الاختبار %d} & %s \\ \hline' % (
    n, ' & '.join(LETTERS[it['key']] for it in items)) for n, items in enumerate(tests, 1))
key = PREAMBLE.replace(r'\cfoot{\thepage/2}', r'\cfoot{}') + r'''\begin{center}
{\Large\khatt\textbf{مفتاح الإجابات ــ الاختبارات من 1 إلى 12}}\\[4pt]
{\small (نسخة الأستاذ ــ لا تُوزَّع على الطلبة)}\\[10pt]
\renewcommand{\arraystretch}{1.8}
\begin{tabular}{|>{\centering\arraybackslash}m{2.2cm}|*{15}{>{\centering\arraybackslash}m{0.62cm}|}}
\hline
\textbf{رقم السؤال} & %s \\ \hline\hline
%s
\end{tabular}

\vspace{10pt}
{\small سلّم التنقيط: نقطة واحدة لكل سؤال (المجموع 15 نقطة). ترتيب الأسئلة: 1--3 سهلة، 4--10 متوسطة، 11--15 صعبة.}
\end{center}
\end{document}
''' % (nums, rows)
with open(os.path.join(here, 'answer_keys.tex'), 'w', encoding='utf-8') as f:
    f.write(key)
print('ok')
