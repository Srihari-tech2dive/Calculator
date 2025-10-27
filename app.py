from flask import Flask, request

app = Flask(__name__)

HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Colorful Math Calculators</title>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background: linear-gradient(125deg, #35baf6 10%, #eef2f3 130%); min-height: 100vh; margin:0; color: #222; }
        h1, nav { background: #0557a8; color: #fff; padding: 24px 0 8px 0; margin: 0; text-align: center; border-radius: 0 0 20px 20px; box-shadow: 0 0px 10px rgba(0,0,0,0.11);}
        nav a {display: inline-block; margin: 0 18px; text-decoration: none; font-weight: bold; color: #fff; font-size: 16px; transition: color 0.2s, background 0.2s; background: #1fa2ff; padding: 8px 18px; border-radius: 20px;}
        nav a:hover {background: #fff; color: #0557a8;}
        .container {margin: 38px auto; max-width: 600px;}
        .calc-group {border-radius: 16px; background: linear-gradient(120deg, #e0c3fc 0%, #8ec5fc 100%); box-shadow: 0 4px 20px rgba(41,81,183,0.09); padding: 24px 36px 30px 36px; margin-bottom: 30px;}
        h2 {font-size: 24px; color: #1b396a; margin-bottom: 18px;}
        label {font-weight: bold; margin-top: 12px; display: block;}
        input[type=text], textarea {padding: 7px 8px; margin-bottom: 16px; margin-top: 3px; font-size: 16px; border-radius: 7px; border: 1px solid #dadada; width: 96%; background: #f2f8fe;}
        button {background: #0575e6; color: #fff; font-weight: bold; border: none; margin:9px 0 16px 0; padding:9px 27px; border-radius: 10px; box-shadow: 0 2px 8px #1fa2ff55; cursor:pointer; font-size: 15px; transition: background 0.18s;}
        button:hover {background: #6dd5ed; color: #0557a8;}
        .result {color: #074; background: #e6fffa; border-radius: 8px; padding: 10px 16px; margin-top: 8px; font-weight: 500; font-size: 15px; box-shadow: 0 1px 8px #b3e1ee55;}
        @media (max-width: 700px) {.container {padding: 0 4%;} .calc-group {padding: 15px 7px 24px 7px;} input[type=text], textarea {width: 99%;}}
        .hide {display:none;}
    </style>
</head>
<body>
<h1>Colorful Math Calculators</h1>
<nav>
  <a href="#" onclick="showCalc('linear');return false;">Linear Dependence</a>
  <a href="#" onclick="showCalc('diag');return false;">Diagonalization</a>
  <a href="#" onclick="showCalc('gauss');return false;">Gauss Jordan</a>
  <a href="#" onclick="showCalc('newton');return false;">Newton Interpolation</a>
  <a href="#" onclick="showCalc('euler');return false;">Euler's Method</a>
</nav>
<div class="container">
<form method="POST" id="linear" class="calc-group {lin_hide}">
    <h2>Linear Dependence</h2>
    <label>Vectors (one per line, space-separated):</label>
    <textarea name="lin_vec" rows="4">{lin_vec}</textarea>
    <button type="submit" name="mode" value="linear">Check</button>
    <div class="result">{lin_result}</div>
</form>
<form method="POST" id="diag" class="calc-group {diag_hide}">
    <h2>Diagonalization</h2>
    <label>Matrix rows (one per line, space-separated):</label>
    <textarea name="diag_matrix" rows="4">{diag_matrix}</textarea>
    <button type="submit" name="mode" value="diag">Diagonalize</button>
    <div class="result">{diag_result}</div>
</form>
<form method="POST" id="gauss" class="calc-group {gauss_hide}">
    <h2>Gauss-Jordan Method</h2>
    <label>Augmented matrix (rows, space-separated, last value is constant):</label>
    <textarea name="gauss_matrix" rows="4">{gauss_matrix}</textarea>
    <button type="submit" name="mode" value="gauss">Solve</button>
    <div class="result">{gauss_result}</div>
</form>
<form method="POST" id="newton" class="calc-group {newton_hide}">
    <h2>Newton's Forward/Backward Interpolation</h2>
    <label>x values (space-separated):</label> <input type="text" name="newton_x" value="{newton_x}">
    <label>y values (space-separated):</label> <input type="text" name="newton_y" value="{newton_y}">
    <label>Value to interpolate:</label> <input type="text" name="newton_val" value="{newton_val}">
    <button type="submit" name="mode" value="newton">Calculate</button>
    <div class="result">{newton_result}</div>
</form>
<form method="POST" id="euler" class="calc-group {euler_hide}">
    <h2>Euler's Method</h2>
    <label>dy/dt expression (use 't' and 'y', e.g. t*y+1):</label> <input type="text" name="euler_expr" value="{euler_expr}">
    <label>Initial t:</label> <input type="text" name="euler_t0" value="{euler_t0}">
    <label>Final t:</label> <input type="text" name="euler_tN" value="{euler_tN}">
    <label>Step size:</label> <input type="text" name="euler_h" value="{euler_h}">
    <label>Initial y:</label> <input type="text" name="euler_y0" value="{euler_y0}">
    <button type="submit" name="mode" value="euler">Solve</button>
    <div class="result">{euler_result}</div>
</form>
</div>
<script>
function showCalc(id){
    ['linear','diag','gauss','newton','euler'].forEach(n=>{
        document.getElementById(n).classList.add('hide');
    });
    document.getElementById(id).classList.remove('hide');
    window.scrollTo({ top: 120, behavior: 'smooth' });
}
// On first page load, show Linear Dependence form
showCalc('{show_form}');
</script>
</body>
</html>
'''

import numpy as np

def render_html(**kwargs):
    # Fill {key} in HTML with value from kwargs, and show one form only
    base = HTML_PAGE
    hide_forms = {f"{n}_hide":'hide' for n in ['linear','diag','gauss','newton','euler']}
    for k,v in kwargs.items(): base = base.replace('{%s}'%k, str(v))
    for k,v in hide_forms.items(): base = base.replace("{%s}"%k, v)
    base = base.replace("{show_form}", kwargs.get("show_form", "linear"))
    # Now unhide the user-selected form
    fkey = kwargs.get('show_form','linear')+"_hide"
    base = base.replace('{%s}'%fkey,'')
    return base

@app.route('/', methods=['GET', 'POST'])
def index():
    # Default values and returned results
    page_data = {
        "lin_vec": "", "lin_result": "", "diag_matrix": "", "diag_result": "",
        "gauss_matrix": "", "gauss_result": "", "newton_x": "", "newton_y": "",
        "newton_val":"", "newton_result":"", "euler_expr":"", "euler_t0":"", "euler_tN":"", "euler_h":"", "euler_y0":"", "euler_result":"",
        "show_form":"linear"
    }
    if request.method == "POST":
        mode = request.form.get('mode','linear')
        page_data['show_form'] = mode
        # --- Linear Dependence ---
        if mode == "linear":
            page_data["lin_vec"] = request.form.get("lin_vec","")
            try:
                rows = [list(map(float, r.strip().split())) for r in page_data["lin_vec"].strip().split('\n') if r.strip()]
                if not rows: page_data["lin_result"]="Invalid input."
                else:
                    matrix = list(zip(*rows))
                    rank = np.linalg.matrix_rank(np.array(matrix))
                    if rank < len(rows):
                        page_data["lin_result"] = "<b style='color:#f00'>Linearly dependent</b>"
                    else:
                        page_data["lin_result"] = "<b style='color:#09b'>Linearly independent</b>"
            except Exception as e:
                page_data["lin_result"] = "Error: "+str(e)
        # --- Diagonalization ---
        elif mode == "diag":
            page_data["diag_matrix"] = request.form.get("diag_matrix","")
            try:
                rows = [list(map(float, r.strip().split())) for r in page_data["diag_matrix"].strip().split('\n') if r.strip()]
                n = len(rows)
                if any(len(r)!=n for r in rows): page_data["diag_result"]="Matrix must be square."
                else:
                    vals, vecs = np.linalg.eig(np.array(rows))
                    vstr=["["+", ".join(f"{v:.3g}" for v in vec)+"]" for vec in vecs.T]
                    page_data["diag_result"] = f"<span style='color:#e11'>Eigenvalues:</span> "+" | ".join(f"{v:.3g}" for v in vals)+"<br><b>Eigenvectors:</b><br>"+"<br>".join(vstr)
            except Exception as e:
                page_data["diag_result"]="Error: "+str(e)
        # --- Gauss-Jordan ---
        elif mode == "gauss":
            page_data["gauss_matrix"] = request.form.get("gauss_matrix","")
            try:
                mat = [list(map(float, r.strip().split())) for r in page_data["gauss_matrix"].strip().split('\n') if r.strip()]
                n = len(mat)
                if any(len(row)!=n+1 for row in mat): page_data["gauss_result"]="Error: must have n+1 numbers per row."
                else:
                    a = np.array(mat)
                    # Apply Gauss-Jordan elimination using numpy
                    for i in range(n):
                        a[i] = a[i] / a[i][i]
                        for j in range(n):
                            if i != j:
                                a[j] = a[j] - a[i] * a[j][i]
                    sol = a[:, -1]
                    page_data["gauss_result"] = "<br>".join([f"<span style='color:#11e;'>x{i+1} = {sol[i]:.4g}</span>" for i in range(n)])
            except Exception as e:
                page_data["gauss_result"]="Error: "+str(e)
        # --- Newton Interpolation ---
        elif mode == "newton":
            page_data['newton_x']=request.form.get('newton_x','')
            page_data['newton_y']=request.form.get('newton_y','')
            page_data['newton_val']=request.form.get('newton_val','')
            try:
                x = [float(z) for z in page_data['newton_x'].split()]
                y = [float(z) for z in page_data['newton_y'].split()]
                val= float(page_data['newton_val'])
                if len(x)!=len(y): page_data["newton_result"]="Error: x and y count mismatch."
                else:
                    n=len(x)
                    f = np.zeros((n, n))
                    f[:,0]=y
                    for j in range(1, n):
                        for i in range(n-j):
                            f[i][j]=(f[i+1][j-1]-f[i][j-1])/(x[i+j]-x[i])
                    sum_=y[0]; u=1
                    for i in range(1, n):
                        u *= (val-x[i-1])
                        sum_ += u * f[0][i]
                    page_data['newton_result'] = f"<span style='color:#db5195;'>Interpolated value: {sum_:.6g}</span>"
            except Exception as e:
                page_data['newton_result'] = "Error: "+str(e)
        # --- Euler's Method ---
        elif mode == "euler":
            page_data['euler_expr']=request.form.get('euler_expr','')
            page_data['euler_t0']=request.form.get('euler_t0','')
            page_data['euler_tN']=request.form.get('euler_tN','')
            page_data['euler_h']=request.form.get('euler_h','')
            page_data['euler_y0']=request.form.get('euler_y0','')
            try:
                expr = page_data['euler_expr']
                t0 = float(page_data['euler_t0'])
                tN = float(page_data['euler_tN'])
                h = float(page_data['euler_h'])
                y0 = float(page_data['euler_y0'])
                def f(t,y): return eval(expr,{"t":t,"y":y,"__builtins__":None})
                t_arr=[t0]; y_arr=[y0]; n=int(np.round((tN-t0)/h))
                for i in range(n):
                    t=t_arr[-1]; y=y_arr[-1]
                    t_arr.append(t+h)
                    y_arr.append(y+h*f(t,y))
                page_data['euler_result']='<span style="color:#db5195;">y values:</span><br>'+"<br>".join([f"<b>t={t_arr[i]:.4g}</b>&nbsp; <span style='color:#09b;'>y={y_arr[i]:.6g}</span>" for i in range(len(y_arr))])
            except Exception as e:
                page_data['euler_result']='Error: '+str(e)

    return render_html(**page_data)

if __name__ == "__main__":
    app.run(debug=True)
