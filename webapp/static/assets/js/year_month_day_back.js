function DateSelector(selYear, selMonth) {
    this.selYear = selYear;
    this.selMonth = selMonth;
    this.selYear.Group = this;
    this.selMonth.Group = this;
    // 给年份、月份下拉菜单添加处理onchange事件的函数
    if (window.document.all != null) // IE
    {
        this.selYear.attachEvent("onchange", DateSelector.Onchange);
        this.selMonth.attachEvent("onchange", DateSelector.Onchange);
    }
    else // Firefox
    {
        this.selYear.addEventListener("change", DateSelector.Onchange, false);
        this.selMonth.addEventListener("change", DateSelector.Onchange, false);
    }

    if (arguments.length == 3)
        this.InitSelector(arguments[3].getFullYear(), arguments[3].getMonth() + 1);
    else if (arguments.length == 5)
        this.InitSelector(arguments[3], arguments[4]);
    else // 默认使用当前日期
    {
        var dt = new Date();
        this.InitSelector(dt.getFullYear(), dt.getMonth() + 1);
    }
}

// 增加一个最大年份的属性
DateSelector.prototype.MinYear = 2015;

// 增加一个最大年份的属性
DateSelector.prototype.MaxYear = (new Date()).getFullYear();

// 初始化年份
DateSelector.prototype.InitYearSelect = function () {
    // 循环添加OPION元素到年份select对象中
    for (var i = this.MaxYear; i >= this.MinYear; i--) {
        // 新建一个OPTION对象
        var op = window.document.createElement("OPTION");

        // 设置OPTION对象的值
        op.value = i;

        // 设置OPTION对象的内容
        op.innerHTML = i;

        // 添加到年份select对象
        this.selYear.appendChild(op);
    }
}

// 初始化月份
DateSelector.prototype.InitMonthSelect = function () {
    // 循环添加OPION元素到月份select对象中
    for (var i = 1; i < 13; i++) {
        // 新建一个OPTION对象
        var op = window.document.createElement("OPTION");

        // 设置OPTION对象的值
        op.value = i;

        // 设置OPTION对象的内容
        op.innerHTML = i;

        // 添加到月份select对象
        this.selMonth.appendChild(op);
    }
}

// 根据年份与月份获取当月的天数
DateSelector.DaysInMonth = function (year, month) {
    var date = new Date(year, month, 0);
    return date.getDate();
}



// 根据参数初始化下拉菜单选项
DateSelector.prototype.InitSelector = function (year, month) {
    // 由于外部是可以调用这个方法，因此我们在这里也要将selYear和selMonth的选项清空掉
    // 另外因为InitDaySelect方法已经有清空天数下拉菜单，因此这里就不用重复工作了
    this.selYear.options.length = 0;
    this.selMonth.options.length = 0;

    // 初始化年、月
    this.InitYearSelect();
    this.InitMonthSelect();

    // 设置年、月初始值
    this.selYear.selectedIndex = this.MaxYear - year;
    this.selMonth.selectedIndex = month - 1;



    }
