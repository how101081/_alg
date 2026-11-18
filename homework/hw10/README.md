# 第10週習題 - 蒙地卡羅隨機法

五題各自獨立成一個 Python 檔，檔名照題號 `monte_carlo_1.py` ～ `monte_carlo_5.py` 排序，只使用標準函式庫。

## 1. `monte_carlo_1.py` - 單變數數值微分與積分

- 微分：中心差分 `(f(x+h) - f(x-h)) / 2h`
- 積分：梯形法，把區間切成 n 個小梯形加總
- 測試 `f(x)=x^2+3x+1` 與 `g(x)=sin(x)`，並印出精確值比較

## 2. `monte_carlo_2.py` - 蒙地卡羅單變數積分

在 `[low, high]` 均勻隨機撒點，以「區間長度 × f 的平均值」估計積分，固定種子方便重現。

## 3. `monte_carlo_3.py` - n 變數數值微分與積分

- `gradient(f, x)`：對每個變數做中心差分得到梯度
- `integral_grid(f, low, high)`：n 維方格中點黎曼和，用來算超體積
- 以三變數 `x^2+y^2+z^2` 示範梯度與單位立方區內的積分

## 4. `monte_carlo_4.py` - 蒙地卡羅 n 變數積分

在 n 維框內隨機取點，以「框體積 × 命中比例」估計超體積，並計算 2、3、5 維單位球體積。

## 5. `monte_carlo_5.py` - `integral(f, low, high)` n 變數積分

- `n = len(low)`，用 n 維方格中點做黎曼和；方格數隨維度指數成長，所以限制總取樣點數約 10000 個（100 維時每軸取 1 格）
- 分別以 1、2、5、100 維計算 `f(x) = x1^2 + ... + xn^2`，範圍取 `[0,1]^n`，精確值為 `n/3`
- 同一題再用蒙地卡羅法 `mc_integral` 計算一次，與黎曼法和精確值比較
- 100 維時黎曼法每軸只能取 1 格，所以結果較粗略；蒙地卡羅法仍接近精確值

## 執行方式

```bash
python monte_carlo_1.py
python monte_carlo_2.py
python monte_carlo_3.py
python monte_carlo_4.py
python monte_carlo_5.py
```
