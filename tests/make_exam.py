"""يولّد الاختبار الموحّد (20 سؤالًا، 4 صفحات) ومفتاح إجاباته من exam_questions.py.

الاستعمال:  python3 make_exam.py   ثم   tectonic exam.tex  و  tectonic exam_key.tex
"""
import os, random, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import tex, LETTERS, ROW_COLORS, PREAMBLE as _P
from exam_questions import EXAM

N = len(EXAM)
assert N == 20
assert [lv for _, lv, _, _ in EXAM] == ['E'] * 4 + ['M'] * 6 + ['H'] * 7 + ['X'] * 3
for _, _, stem, opts in EXAM:
    assert len(opts) == 5 and len(set(opts)) == 5, stem

# مواضع الإجابات الصحيحة: كل حرف 4 مرات
rng = random.Random(1962)
pos = [0, 1, 2, 3, 4] * 4
rng.shuffle(pos)
items = []
for (ch, lv, stem, opts), p in zip(EXAM, pos):
    wrong = opts[1:]
    rng.shuffle(wrong)
    items.append(dict(stem=stem, opts=wrong[:p] + [opts[0]] + wrong[p:], key=p))

out = [_P.replace('@PAGES@', '4').replace('[11pt,a4paper]', '[10pt,a4paper]').replace('Scale=1.08', 'Scale=1.0').replace('left=1.3cm,right=1.3cm', 'left=1.2cm,right=1.2cm'), r'''\begin{center}
{\LARGE\khatt\textbf{الاختبار في الذكاء الاصطناعي}}\\[3pt]
{\normalsize أسئلة متعددة الاختيارات ــ الفصول من 1 إلى 6 ــ 20 سؤالًا}
\end{center}
\vspace{-4pt}\rule{\textwidth}{0.6pt}\\
{\small\textbf{التعليمة:} لكل سؤال إجابة صحيحة واحدة فقط من بين خمسة اختيارات؛ اقرأ الاختيارات كلها بعناية قبل الإجابة.
اكتب \textbf{حرف} الإجابة الصحيحة في جدول الإجابات أسفل الصفحة الأخيرة.
لكل سؤال نقطة واحدة (المجموع 20 نقطة).}
\vspace{-2pt}
\begin{multicols}{2}
''']
for n, it in enumerate(items, 1):
    out.append(r'\noindent\begin{minipage}{\linewidth}')
    out.append(r'\hangindent=0.7cm\hangafter=1\makebox[0.7cm][r]{\textbf{%d.}}\textbf{%s}' % (n, tex(it['stem'])))
    out.append(r'\begin{itemize}[leftmargin=0.95cm, labelsep=4pt, itemsep=1pt, topsep=3pt, parsep=0pt]')
    for i, o in enumerate(it['opts']):
        out.append(r'  \item[\textbf{%s)}] %s' % (LETTERS[i], tex(o)))
    out.append(r'\end{itemize}')
    out.append(r'\end{minipage}\par\vspace{8pt plus 6pt}')

nums = ' & '.join(r'\textbf{%d}' % i for i in range(1, N + 1))
blanks = ' & '.join([''] * N)
cols = r'|>{\centering\arraybackslash}m{1.9cm}|*{%d}{>{\centering\arraybackslash}m{0.5cm}|}' % N
out.append(r'''\end{multicols}
\vfill
\begin{center}
{\khatt\textbf{جدول الإجابات}}\\[3pt]
\renewcommand{\arraystretch}{1.6}\setlength{\tabcolsep}{2.5pt}
\begin{tabular}{%s}
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
''' % (cols, nums, blanks))

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, 'exam.tex'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

# ---------- مفتاح الإجابات ----------
keys = ' & '.join(LETTERS[it['key']] for it in items)
key = _P.replace(r'\cfoot{\thepage/@PAGES@}', r'\cfoot{}') + r'''\begin{center}
{\Large\khatt\textbf{مفتاح الإجابات ــ الاختبار في الذكاء الاصطناعي}}\\[4pt]
{\small (نسخة الأستاذ ــ لا تُوزَّع على الطلبة)}\\[10pt]
\renewcommand{\arraystretch}{1.9}\setlength{\tabcolsep}{2.5pt}
\begin{tabular}{%s}
\hline
\rowcolor{%s}\textbf{رقم السؤال} & %s \\ \hline
\rowcolor{%s}\textbf{الإجابة} & %s \\ \hline
\end{tabular}

\end{center}
\end{document}
''' % (cols, ROW_COLORS[7], nums, ROW_COLORS[4], keys)
with open(os.path.join(here, 'exam_key.tex'), 'w', encoding='utf-8') as f:
    f.write(key)
print('ok')
