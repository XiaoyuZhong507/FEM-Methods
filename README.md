# 有限元方法 · 课程资料与作业

研究生「有限元方法」课程的学习资料整理：教材定位、作业转录与解答、一维 P1 有限元的可复现程序。

## 目录结构

```
有限元方法/
├─ 教材/                          教材 PDF（5 本，**不进仓库**，见下）
├─ 作业/                          hw1、hw3、hwcode1、hwcode3（4 份 PDF）
│                                + 一张新作业照片（二维 P2 三角形网格，尚未编号）
├─ 整理/
│  ├─ 教材与作业整理.md            主文档：教材地图 + 页码口径 + 作业逐题定位
│  ├─ 作业解答/hw1解答.md          hw1 四题完整解答（推导 + 回代检验 + 可追问点）
│  └─ 作业代码/fem1d_p1.py        一维 P1 有限元，两个程序作业共用一个脚本
└─ .dsh/skills/course-notes-profile/
                                 课程档案（B 层）：资料源、坐标记号、取舍范围、产物索引
```

## 快速开始

```powershell
# 复现 hwcode1 / hwcode3 的误差与收敛阶表
python 整理/作业代码/fem1d_p1.py
```

需要 `numpy`。脚本对两种边界条件（齐次 Dirichlet、纯 Neumann）各输出一张
`N | L² error | order | H¹ error | order` 表，阶数应与理论一致：L² 为 2，H¹ 为 1。

## 教材不纳入版本管理

`教材/` 下 5 本 PDF 共 61.8 MB，已写入 `.gitignore`。它们的**位置、页数、文本层状况、
PDF 页序与印刷页的偏移**都记录在 `整理/教材与作业整理.md` 与课程档案里，换机器时按档案重新获取即可。

| 教材 | 页数 | 文本层 | 定位 |
|---|---|---|---|
| Johnson, *Numerical Solution of PDEs by the FEM* | 278 | 无（扫描件） | 计算主线 |
| Brenner & Scott, *The Mathematical Theory of FEM* | 403 | 良好 | 理论主线 |
| Ciarlet, *The FEM for Elliptic Problems* | 559 | 可读（含乱码） | 严格参考 |
| Boffi–Brezzi–Fortin, *Mixed FEM and Applications* | 691 | 良好 | 进阶 |
| Briggs–Henson–McCormick, *A Multigrid Tutorial* | 206 | 良好 | 拓展 |

## 连接远程仓库

在 GitHub 上建一个**私有**空仓库（课程资料与老师发的题目不要公开），然后：

```powershell
git remote add origin https://github.com/<你的用户名>/fem-course.git
git push -u origin main
```

## 备注

- 作业编号为 `hw1`、`hw3`、`hwcode1`、`hwcode3`，**`hw2`/`hwcode2` 缺失**，按原样保留未补号。
- 引用教材页码时注意 PDF 页序 ≠ 印刷页：Brenner +14、Boffi +15、Ciarlet +29、Johnson +0、Multigrid +13。
- `hwcode3` 的刚度矩阵奇异（核为常数），程序里固定 `u_h(0)=0` 定规范；不处理会让 L² 误差不收敛。
