# 有限元方法 · 课程资料与作业

研究生「有限元方法」课程的学习资料整理：5 次作业的题目与答卷归档、一维/二维有限元的可复现程序、以及一套随课程推进自动维护的资料档案。

## 目录结构

```
有限元方法/
├─ 教材/                                教材 PDF（5 本，**不进仓库**，见下）
├─ 作业/有限元作业1-5/
│  ├─ 作业1/   1D 齐次 Dirichlet，P1     原题 hw1.pdf / hwcode1.pdf，答卷 + hw1.m
│  ├─ 作业2/   1D 纯 Neumann，P1         原题 hw3.pdf / hwcode3.pdf，答卷 + hw2.m
│  ├─ 作业3/   Sobolev 理论（Brenner 1.x.1–1.x.16）
│  ├─ 作业4/   2D 三角形网格，P1         原题 hwcode4.pdf，报告 + 两张输出图
│  └─ 作业5/   1D P2（端点+中点）        原题 hwcode2.pdf，报告 + hw2d.m
├─ 整理/
│  ├─ 教材与作业整理.md                  主文档：教材地图 + 页码口径 + 5 次作业台账
│  ├─ 作业解答/hw1解答.md                hw1 四题完整解答（推导 + 回代检验 + 可追问点）
│  └─ 作业代码/fem1d_p1.py               一维 P1 有限元（Dirichlet / Neumann 切换）
└─ .dsh/skills/course-notes-profile/     课程档案（B 层）：资料源、编号定位、取舍、产物、提示词
```

## 快速开始

```powershell
# 复现 1D P1 的误差与收敛阶表（对应作业1、作业2 的程序部分）
python 整理/作业代码/fem1d_p1.py
```

需要 `numpy`。脚本对两种边界条件各输出一张 `N | L² error | order | H¹ error | order` 表，
阶数应与理论一致：$P^1$ 的 $L^2$ 为 2、$H^1$ 为 1。

> 原答卷用**北太天元（Baltamatica）**写成（`作业N/*.m`），与本脚本的实现细节有差异：
> 答卷里 `hw1.m` 的 $N$ 是**内节点数**（$h=1/(N+1)$），本脚本的 $N$ 是**单元数**（$h=1/N$）。
> 两者都正确，但表格数值不能逐位对齐。

## 教材不纳入版本管理

`教材/` 下 5 本 PDF 共 61.8 MB，已写入 `.gitignore`。它们的位置、页数、文本层状况、
PDF 页序与印刷页的偏移，都记录在 `整理/教材与作业整理.md` 与课程档案里。

| 教材 | 页数 | 文本层 | 定位 |
|---|---|---|---|
| Johnson, *Numerical Solution of PDEs by the FEM* | 278 | 无（扫描件） | 计算主线（作业5 引用第 82 页习题 3.1） |
| Brenner & Scott, *The Mathematical Theory of FEM* | 403 | 良好 | 理论主线（习题编号 `1.x.N`） |
| Ciarlet, *The FEM for Elliptic Problems* | 559 | 可读（含乱码） | 严格参考 |
| Boffi–Brezzi–Fortin, *Mixed FEM and Applications* | 691 | 良好 | 进阶 |
| Briggs–Henson–McCormick, *A Multigrid Tutorial* | 206 | 良好 | 拓展 |

## 已知问题

- **编号不对应**：作业文件夹序号与文件编号不一致（`作业2/` 装 `hw3.pdf`、`作业5/` 装 `hwcode2.pdf`），按原样保留，对照表见 `整理/教材与作业整理.md` §一。
- **教材副本重复**：`作业5/` 里夹带 `johnson_FEM.pdf`(10.9 MB) 与 `Brenner_FEM.pdf`(2.8 MB)，与 `教材/` 下 MD5 相同，建议删除。
- **作业4 书面未完成**：`作业4书面.docx` 只有标题「1.x.20 解：」，正文为空。
- **作业4 的 P1/P2 存疑**：`hwcode4.pdf` 要求 $P^1$，但曾出现一张要求 $P^2$（顶点+边中点）的照片，待向老师确认。

## 连接远程仓库

```powershell
git remote -v            # 已配置 origin
git add -A && git commit -m "说明" && git push
```

课程材料建议保持**私有仓库**。
