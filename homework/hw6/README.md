# 習題 6：Lambda Calculus 解譯器

課程：演算法 | 學生：楊丞皓 | 學號：06

---

## 什麼是 Lambda Calculus

其實只有三種東西：

| 東西 | 寫法 | 意思 |
|------|------|------|
| 變數 | `x` | 就是一個名字 |
| 函數 | `\x.body` | 吃一個參數 x，回傳 body |
| 套用 | `(f a)` | 把 f 套用到 a |

計算規則只有一條 beta reduction：`(\x.body) a` 就把 body 裡的 x 全部換成 a。一直換到不能換就是答案。我用的策略是**最左最外優先**（normal order）。

## 程式怎麼寫的

1. `parse()`：把字串拆成語法樹（三種節點 Var / Lam / App）
2. `subst()`：做上面那個「換掉 x」的動作，如果名字會撞到就自動改名（alpha rename）
3. `step()`：找最左最外可以化簡的地方，做一次
4. `run()`：一直 `step()` 並把每一步印出來

## 執行結果

```
$ python lambda.py
```

### 1. 身分函數

```
(\x.x) (\y.y)
= (λy.y)
（沒有可化簡的了，這就是答案）
```

### 2. 邏輯：TRUE AND FALSE

`AND = \p.\q.p q p`，TRUE = `\x.\y.x`，FALSE = `\x.\y.y`

```
AND TRUE FALSE
= ...（中間每一步都印出來）
= (λx.(λy.y))      也就是 FALSE ✓
```

### 3. 後繼函數：SUCC 1

`SUCC = \n.\f.\x.f (n f x)`，1 = `\f.\x.f x`

```
SUCC 1
= ...（中間每一步）
= (λf.(λx.(f (f x))))   也就是 2 ✓
```

### 4. 加法：ADD 1 1

`ADD = \m.\n.\f.\x.m f (n f x)`

```
ADD 1 1
= ...（中間每一步）
= (λf.(λx.(f (f x))))   也就是 2 ✓
```

四個例子都一步一步印出來，最後的答案也對（邏輯變 FALSE、數字 1 變 2）。

---

## AI 使用

題目說可以用 AI，我用的 AI 是 opencode（big-pickle 模型）。過程大概是我先講清楚需求（要印完整過程、要短、50 分鐘做得完），然後跟它一起把 parser、subst、step 三個小函式寫出來，再自己跑測試看 church numeral 有沒有算對。
