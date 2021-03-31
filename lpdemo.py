<form action="{{ url_for("gfg")}}" method="post"> 
            <label for="objective_function">Enter Objective Function: <br></br></label> 
            <input type="text" id="objective_function" name="objfunc" placeholder="Format: Maximize 8x1+5x2"> 
            <br></br>  
            <label for="constraints">Enter Constraints (Format: 2x1+x2<=1000,3x1+4x2<=2400): <br></br> </label> 
            <input type="text" id="constraints" name="constr" placeholder="Constraint List"> 
            <br></br>
            <button type="submit">Solve</button> 
</form>


ans=None
@app.route('/', methods =["GET", "POST"]) 
def gfg(ans=""): 
    if request.method == "POST": 
       # getting input with name = fname in HTML form 
       objfunc = request.form.get("objfunc") 
       # getting input with name = lname in HTML form  
       constr = request.form.get("constr") 
       #ans = demo_main(objfunc+constr) 
       ans = main(objfunc, constr)
       ans=json.dumps(ans, indent=1)
       #return ans
    return render_template(
        "form.html",
        result=ans
    ) 