# 怎麼用 BCM：use case 評估、readiness、value stream、ongoing governance

> [`bcm-製作重點.md`](./bcm-製作重點.md) 教「怎麼畫一張 BCM」。這份教「畫完之後怎麼用、怎麼養」——因為 BCM 不是畫完存檔的文件，是 **ongoing governance backbone**。方法源自 01 場 [`../01-ai-journey-business-capability-maps/notes.md`](../01-ai-journey-business-capability-maps/notes.md)。

## 0. 畫完不是結束，是起點

畫完只是有了底圖。價值在拿它當「全公司 AI 治理的對話單位」。最常見的死法：BCM 一次性建完、存進 SharePoint、三年沒人看。**沒 cadence 的 BCM 就是一張死掉的圖。**

## 1. 完整鏈：Capability → Value Stream → Process → IT system

BCM 只列能力、沒講順序（像一盒 Lego，有方塊但不知道哪個先）。要 operationalize 就往下接：

- **Value Stream（也是一種圖）**：把 capability 串成「為了 deliver X outcome，依序通過 A→B→C」的流；每個 capability 在流上有 KPI、input、output、dependency。**BCM 是 box，value stream 是 arrow**。通常從 BCM 的 L2–3 出發（L1 太抽象不適合排序）。
- **Process**：在某條 value stream 上，這條 capability 具體怎麼跑。
- **IT system**：process 再往下對應到 application、data source、integration。

每層對齊上層。BCM 沒做好就直接做 process model＝蓋房子從中間樓層開始。

## 2. Digital Thread：讓資料治理＝業務治理

把 value stream 對應到 data flow——每個 capability transition 都伴隨資料的轉換與移動。一路看下去：「客戶下單」這條 value stream 觸發哪些資料表更新、哪些 system call、哪些 model 預測。**Digital thread 讓「資料治理」跟「業務治理」變成同一回事，不是兩條平行線。**

## 3. 每個 capability 一張 metadata 卡（governance 的真正單位）

BCM 不只是 box。每個 capability 底下一張卡：**definition／responsible owner（單一）／data input／data output／supporting systems**。沒填 metadata 的 BCM 是裝飾品；填了才能 drive 投資決策、責任歸屬、跨部門溝通。

（這正是 bcm-creator 功課裡標「待補」的那四欄——owner／systems／data in-out 非公開，要組織自己填。功課把公開那半填好、留好格子等內部補。）

## 4. Data readiness 是 contextual 的

Readiness 不是「資料零錯誤」，是「每個 capability 對 data 的需求是什麼？我們的結構支援嗎？」分 1–5 級。**同一份資料對 A capability 可能是 5 級、對 B 可能是 2 級**。等資料 100% 乾淨才開始 AI 投資的公司，永遠不會開始。

## 5. BCM × use case：把 AI 釘在能力上（Opportunity Radar）

有了 BCM，把 AI use case 映射上去（**AI Opportunity Radar**，四象限：core capability／back office／product & services／front office）。**釘在 capability、不釘在 use case 本身**——use case 半年過時，capability 三五年不變。一眼看出投資集中在哪、忽略了哪、組合平不平衡。

## 6. 每個 use case 拆 6 維 agent 能力

評一個 AI use case／vendor 的 agent，拆 6 維：**Perception（看／聽／讀）、Decisioning（決策）、Actioning（執行）、Agency（自主度）、Adaptability（適應）、Knowledge（知識存取）**。多數 use case 只需其中 2–3 維強。用這 6 維評，比聽 vendor 講「我們有 agentic AI」可靠十倍。

## 7. Agency 警告：自動決策出錯會擴散

Agency 是 5 級光譜、不是開關。**Level 1 fully autonomous 在多數產業是科幻**——end-to-end value chain 太複雜，任何一個自動決策出錯都會擴散。selective process（單一機械動作）可以 Level 1，end-to-end 不行。多數企業合理停在 Level 3–4，那不是失敗、是務實。

## 8. 每個 use case 問清楚：技術 + 資料源 + 整合工程

一個 use case 從來不是「用一個 AI」做的。簽案／評估前問清楚：**需要哪幾種 AI 技術 + 哪幾個資料源 + 哪些整合工程**。不是每個 use case 都要 Gen AI——選錯不只浪費錢，還會把 deterministic 流程灌入 probabilistic 行為，準確率比舊系統還差。沒問清楚，POC 跑得起來但 production 跑不動。

## 9. AI Readiness（7 維，看 gap 不看分數）

起步前評 readiness，7 維：**Strategy／Value／Organization／People & Culture／Governance／AI Engineering／AI Data**，每維 1–5。**重點不是當前分數，是 current vs future 的 gap**。多數組織誤以為 readiness 就是「人才＋資料」兩維，忽略 Strategy 跟 Governance——這是後期 scale 不出去的主因。Future state 通常被高估，要有 case 支撐、不是拍腦袋；找不到任何案例證明你的 vision 可行，那不是 vision，是幻覺。

## 10. 每個 use case 上 Defend／Extend／Upend 標籤（對）

是的，AI business case 上這三種標籤：

- **Defend**：augment 既有員工、不改流程結構，ROI 穩、好算（AI 寫 code／JD／文案）。低風險、低天花板。
- **Extend**：改寫 process、有 vendor packaged solution、ROI 算得出（客服自動化、保險 claims auto-approval）。enterprise 主戰場。
- **Upend**：frontier，連 value 存不存在都不確定（藥物開發）。高風險高回報，需 patience capital。

三型組合才健康——全押 Defend 三年沒差異化、全押 Upend 燒光現金。

## 11. AI strategy ≠ IT strategy 的子集

AI 對 business model 跟 operating model 影響太深，要**獨立規劃**。沒 AI strategy 的公司會失去競爭力；但 **bad AI strategy 的公司會直接受傷**（合規、信任、客戶體驗）。BCM 是承載 AI strategy 的底圖。

## 12. Bimodal：top-down 接 bottom-up（POC 失敗的真因）

- **Top-down（leadership 帶）**：BCM、use case prioritization、readiness assessment——strategic 動作。
- **Bottom-up（team 親手做）**：POC、prototype、end-user pilot——operational 動作。

兩條同時跑才對。**很多 team 的 POC 失敗，不是做不出來，是沒接上 BCM**：POC 一上線就沒人持續 track，三個月後沒人記得當初 KPI 訂在哪——因為 KPI 沒掛在任何 capability 上。BCM 是把 POC 釘在組織骨幹上的那根釘子；只走 top-down 是 PPT 治理，只走 bottom-up 是無頭蒼蠅。

## 13. Update BCM 的動作流程（cadence）

BCM 是 ongoing governance backbone，**排進行事曆、每季或半年回看**。一次回看跑這幾步：

1. **Pace 重評** — 每個 capability 對主要 objective 的 pace 還對嗎？去年 keep up 的，今年對手都 AI 化了 → 升 differentiating？
2. **Use case 狀態** — radar 上的 use case 有沒有從 calculated risk 進到 likely win（feasibility 成熟了）？
3. **Readiness gap** — 哪些 capability 的 data／AI readiness 進步了、gap closed？
4. **POC 接線（最常漏的一步）** — 每個跑過的 POC 釘回對應 capability + KPI；上線的有沒有持續 track？沒 track 的標紅。
5. **Metadata 更新** — owner 換人？supporting systems 換了？data readiness 變了？
6. **新增／退役** — 新商業模式帶出新 capability？哪條 capability 變 commodity（該外包）？
7. **重生功課＋圖** — 資料變了就重跑 bcm-creator 更新 input 功課 + image，標版本與日期。

AI 一直變，定格的 BCM 撐不過一年。

## 恍然大悟

BCM 真正在做的，是把 AI 從「IT 部門的一個 PoC」拉回「全公司的策略治理」。Process map 太細、product roadmap 太窄、project plan 太短——只有 BCM 同時「夠抽象 C-level 看得懂」「夠具體可 attach 投資」「夠穩定撐 multi-year 對話」。它不是取代你既有工具，是把它們串起來的那條線。沒這條線，AI 投資永遠是孤島 POC 的合集；有這條線，AI 投資是組織能力的 compound growth。
