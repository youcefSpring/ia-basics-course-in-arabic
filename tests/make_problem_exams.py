"""يولّد 30 اختبارًا (وضعيات إشكالية، 5 أسئلة لكل منها، عمود واحد) ومفتاح إجاباتها
من problem_questions.py (الاختبارات 1–5) و problem_questions_XX_YY.py (الاختبارات 6–30).

الاستعمال:  python3 make_problem_exams.py   ثم   tectonic problem_exam_XX.tex  و  tectonic problem_exams_key.tex
"""
import os, random, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import tex, LETTERS, ROW_COLORS, PREAMBLE as _P
import importlib
from problem_questions import PROBLEMS as _P1
PROBLEMS = list(_P1)
for _m in ['06_10', '11_15', '16_20', '21_25', '26_30']:
    PROBLEMS += importlib.import_module('problem_questions_' + _m).PROBLEMS

N_EXAMS, N_Q = 30, 5
ORD = ['الأول', 'الثاني', 'الثالث', 'الرابع', 'الخامس', 'السادس', 'السابع', 'الثامن', 'التاسع',
       'العاشر', 'الحادي عشر', 'الثاني عشر', 'الثالث عشر', 'الرابع عشر', 'الخامس عشر',
       'السادس عشر', 'السابع عشر', 'الثامن عشر', 'التاسع عشر', 'العشرون', 'الحادي والعشرون',
       'الثاني والعشرون', 'الثالث والعشرون', 'الرابع والعشرون', 'الخامس والعشرون',
       'السادس والعشرون', 'السابع والعشرون', 'الثامن والعشرون', 'التاسع والعشرون', 'الثلاثون']

for e, ch, stem, opts in PROBLEMS:
    assert len(opts) == 5 and len(set(opts)) == 5, stem
exams = [[p for p in PROBLEMS if p[0] == n] for n in range(1, N_EXAMS + 1)]
assert all(len(x) == N_Q for x in exams) and len(PROBLEMS) == N_EXAMS * N_Q
assert len({p[2] for p in PROBLEMS}) == len(PROBLEMS)  # لا تكرار للوضعيات

# مواضع الإجابات الصحيحة: في كل اختبار تكون الحروف الخمسة مختلفة (كل حرف مرة واحدة)
rng = random.Random(2026)
all_items = []
for qs in exams:
    pos = list(range(5))
    rng.shuffle(pos)
    items = []
    for (_, ch, stem, opts), p in zip(qs, pos):
        wrong = opts[1:]
        rng.shuffle(wrong)
        items.append(dict(ch=ch, stem=stem, opts=wrong[:p] + [opts[0]] + wrong[p:], key=p))
    all_items.append(items)

PREAMBLE = (_P.replace(r'\cfoot{\thepage/@PAGES@}', r'\cfoot{\thepage/\pageref{LastPage}}')
              .replace(r'\usepackage{fancyhdr}', r'\usepackage{fancyhdr}' + '\n' + r'\usepackage{lastpage}')
                            .replace('top=1.6cm,bottom=1.4cm', 'top=1.7cm,bottom=1.5cm')
              .replace('left=1.3cm,right=1.3cm', 'left=1.5cm,right=1.5cm'))


def question(n, it):
    out = [r'\noindent',
           r'{\large\khatt\textbf{الوضعية %d}}\hfill{\small(الفصل %d)}\par\nopagebreak\vspace{3pt}' % (n, it['ch']),
           r'\setlength{\fboxsep}{7pt}\colorbox{gray!10}{\parbox{\dimexpr\linewidth-14pt}{%s}}\par\nopagebreak' % tex(it['stem']),
           r'\begin{itemize}[leftmargin=1.0cm, labelsep=6pt, itemsep=3pt, topsep=4pt, parsep=0pt]']
    for i, o in enumerate(it['opts']):
        out.append(r'  \item[\textbf{%s)}] %s' % (LETTERS[i], tex(o)))
    out += [r'\end{itemize}']
    return '\n'.join(out)


def exam_tex(n, items):
    out = [PREAMBLE, r"""\linespread{1.08}\selectfont
\begin{center}
{\LARGE\khatt\textbf{الاختبار %s في الذكاء الاصطناعي}}\\[4pt]
{\normalsize وضعيات إشكالية ــ أسئلة متعددة الاختيارات ــ الفصول من 1 إلى 6}
\end{center}
\vspace{-2pt}\rule{\textwidth}{0.6pt}\\[2pt]
\textbf{التعليمة:} يتضمن الاختبار خمس وضعيات إشكالية. اقرأ كل وضعية بعناية، ثم اختر التحليل أو التصرف الأنسب
من بين الاختيارات الخمسة؛ لكل وضعية إجابة صحيحة واحدة فقط.
اكتب \textbf{حرف} الإجابة الصحيحة في جدول الإجابات في آخر الاختبار.
لكل وضعية 4 نقاط (المجموع 20 نقطة).
\vspace{4pt}
""" % ORD[n - 1]]
    # تدفق متصل دون فراغات أو فواصل صفحات إجبارية
    for q in range(N_Q):
        out.append(question(q + 1, items[q]))
        out.append(r'\par\vspace{6pt}')
    nums = ' & '.join(r'\textbf{%d}' % i for i in range(1, N_Q + 1))
    blanks = ' & '.join([''] * N_Q)
    out.append(r"""\begin{center}
{\khatt\textbf{جدول الإجابات}}\\[3pt]
\renewcommand{\arraystretch}{1.6}
\begin{tabular}{|>{\centering\arraybackslash}m{1.9cm}|*{%d}{>{\centering\arraybackslash}m{1.2cm}|}}
\hline
\textbf{رقم السؤال} & %s \\ \hline
\textbf{الإجابة} & %s \\[8pt] \hline
\end{tabular}

\vspace{8pt}
\renewcommand{\arraystretch}{2.2}
\begin{tabular}{|>{\centering\arraybackslash}m{7.5cm}|>{\centering\arraybackslash}m{3.2cm}|>{\centering\arraybackslash}m{3.2cm}|}
\hline
\textbf{الاسم واللقب} & \textbf{الفوج} & \textbf{العلامة} \\ \hline
 & & \hfill /20 \\ \hline
\end{tabular}
\end{center}
\end{document}
""" % (N_Q, nums, blanks))
    return '\n'.join(out)


here = os.path.dirname(os.path.abspath(__file__))
for n, items in enumerate(all_items, 1):
    with open(os.path.join(here, 'problem_exam_%02d.tex' % n), 'w', encoding='utf-8') as f:
        f.write(exam_tex(n, items))

# ---------- مفتاح الإجابات ----------
nums = ' & '.join(r'\textbf{%d}' % i for i in range(1, N_Q + 1))
rows = '\n'.join(r'\rowcolor{%s}\textbf{الاختبار %d} & %s \\ \hline' % (
    ROW_COLORS[(n - 1) % len(ROW_COLORS)], n, ' & '.join(LETTERS[it['key']] for it in items))
    for n, items in enumerate(all_items, 1))
key = _P.replace(r'\cfoot{\thepage/@PAGES@}', r'\cfoot{}') + r'''\begin{center}
{\Large\khatt\textbf{مفتاح الإجابات ــ اختبارات الوضعيات الإشكالية من 1 إلى 30}}\\[4pt]
{\small (نسخة الأستاذ ــ لا تُوزَّع على الطلبة)}\\[10pt]
\renewcommand{\arraystretch}{1.45}
\begin{tabular}{|>{\centering\arraybackslash}m{3.2cm}|*{%d}{>{\centering\arraybackslash}m{1.4cm}|}}
\hline
\textbf{رقم الوضعية} & %s \\ \hline\hline
%s
\end{tabular}
\end{center}
\end{document}
''' % (N_Q, nums, rows)
with open(os.path.join(here, 'problem_exams_key.tex'), 'w', encoding='utf-8') as f:
    f.write(key)
print('ok')
