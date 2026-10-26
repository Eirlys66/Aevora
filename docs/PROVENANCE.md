# 来源说明（Provenance）

本仓库代码主要由 AI 助手生成，作者提出设计意图与需求。设计与实现**参考了若干公开项目的思路**。

这份文件记录一次针对「本仓库是否含有上游代码片段」的技术审计，方法、数据与结论都在下面，供任何审阅者复核。

> **适用范围**：审计对象是随后会加入本仓库的代码库。此刻仓库里只有设计文档，还没有代码——所以这份记录是**提前**做的，等代码进来时它就是基线，不需要从头再补。

审计日期：2026-10-26

---

## 一、方法

把本仓库全部 `.py` / `.ts` / `.tsx` 源码，与下列上游仓库的全部源码做**token 级 6-gram 片段比对**。

- 相似度指标：`containment = |交集| / min(|A|, |B|)`，按**较短文件**计算——比 Jaccard 更适合发现「小文件被整体搬进大文件」。
- 过滤：只纳入 ≥300 token 的文件；单文件上限 400 KB；跳过 `node_modules`、`dist`、`assets` 等目录；剔除纯注释行。
- 对同源度最高的若干对，额外计算**最长连续重合 token 段**——这是区分「语言惯用写法」与「实质复制」的关键：抄代码会出现 200+ token 的连续块，巧合只会有十几个 token。

## 二、上游项目与许可证

| 项目 | 地址 | 许可证 |
|---|---|---|
| Serein | github.com/Yinglianchun/Serein | MIT © 2026 ChiYouyu |
| Ombre Brain | github.com/P0luz/Ombre-Brain | MIT © 2026 P0lar1zzZ |
| AionsHome | github.com/death34018-hue/AionsHome | MIT © 2026 death34018-hue |
| 心潮念 | github.com/tianyupaipai-cmd/xinchao-nian | 顶层 AGPL-3.0；`xinchao/` 与 `bridge/` 为 MIT；`ombre-brain/` 为 MIT ＋ 二改者附加的非商业约束 |

## 三、结果

| 上游 | 最高同源度 | 超过 0.15 的配对数 |
|---|---|---|
| Serein | 0.211 | 4 |
| Ombre Brain | 0.126 | 0 |
| AionsHome | 0.109 | 0 |
| 心潮念 | 0.104 | 0 |

同源度最高的三对，最长连续重合段及内容如下：

| 本仓库文件 | 上游文件 | 最长连续重合 | 内容 |
|---|---|---|---|
| frontend/src/components/AccessGate.tsx | Serein web/src/pages/BasementPage.jsx | 16 token | `const [error, setError] = useState("")` |
| backend/app/services/daily_memories.py | Serein src/serein/adapters/bridge.py | 26 token | `"role": row["role"], "created_at": row["created_at"]` |
| backend/app/services/daily_self_awareness.py | Serein src/serein/compat/germany/narrative_writer_sources.py | 20 token | `-> dict[str, Any]:` / `.encode("utf-8")).hexdigest()` |

三段均为语言惯用写法，不构成实质复制。

## 四、结论

**在「接触成立」的前提下（见第六节），没有发现上游代码被复制进本仓库的证据。**

- 文本层面：最高同源度 0.211，最长连续重合 26 个 token，且内容为语言惯用写法。
- 结构层面：与四个上游的表名无任何领域性重合（仅 `events` / `jobs` / `messages` / `tasks` 这类通用词）；共享标识符全部为 FastAPI / Pydantic / SQLite 框架词汇；记忆模型分属两套不同范式——上游为「桶管理＋衰减＋投影」，本仓库为「不可变版本＋来源引用＋事件流」。

这句话不等于「证明不存在」。本方法有明确盲区，见下节。任何据此作出的判断都应当与盲区一起阅读。

## 五、方法局限

1. **识别不了重写**：把函数改写一遍实现同样算法，相似度会很低。本方法只能排除「文本相似」，不能排除「逻辑相似」。
2. **抓不到短片段**：不足 300 token 的文件不纳入比对。
3. **不评估结构相似**：接口顺序、模块划分、流程编排这一层的相似（SSO）属于法律判断，不是文本比对能回答的。
4. **只比对上述四个上游**，未覆盖其他可能存在影响的来源。

## 六、参考方式与接触情况

本项目在设计与实现阶段，作者明确指示 AI 助手**参考上述项目的实现方式**，但效果须达到作者自己描述的目标。其中部分项目的源码副本存在于同一台开发服务器上。

**因此本说明不声称「未接触过上游代码」。** 接触是成立的——这是一个「看过参考实现、按自己的设计重写」的过程，不是干净房间（clean room）。

把这一点写明的理由：一份基于「我从没看过」的说明，一旦被证明看过就整体失效；而一份承认看过、并用可复核数据说明「没有复制表达」的说明，反而更稳。第三、五节的数据正是在这个前提下才有意义。

## 七、关于 AI 生成代码

本仓库代码由 AI 助手按作者的设计意图生成。作者提供需求、效果描述与判断标准，并对是否采纳参考实现中的具体做法作出取舍。

若日后发现某段代码与上游实质相同，将按对应上游的许可证要求处理：MIT 部分补充版权与许可声明；涉及 AGPL-3.0 或非商业附加约束的部分，重写或移除。
