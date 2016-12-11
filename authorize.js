STK.register("common.listener", function (b) {
    var c = {};
    var a = {};
    a.define = function (e, f) {
        if (c[e] != null) {
            throw "common.listener.define: 频道已被占用"
        }
        c[e] = f;
        var d = {};
        d.register = function (h, g) {
            if (c[e] == null) {
                throw "common.listener.define: 频道未定义"
            }
            b.core.util.listener.register(e, h, g)
        };
        d.fire = function (g, h) {
            if (c[e] == null) {
                throw "commonlistener.define: 频道未定义"
            }
            b.core.util.listener.fire(e, g, h)
        };
        d.remove = function (h, g) {
            b.core.util.listener.remove(e, h, g)
        };
        return d
    };
    return a
});
STK.register("common.channel.sso", function (a) {
    return a.common.listener.define("common.channel.sso", ["login", "login_complete", "login_success", "login_failure", "logout", "logout_complete", "logout_success", "logout_failure", "verify", "need_verify"])
});
STK.register("common.util.sso", function (d) {
    var e, c = d.core.json.merge,
        a = sinaSSOController,
        b = d.common.channel.sso;
    return function (f) {
        var h = {};
        f = f || {};
        var g = c({
            savestate: 0,
            vsnf: 0,
            hold_login_state: true,
            cookie_timeout: 1800,
            entry: "sinaoauth",
            domain: "sina.com.cn",
            service: "sinaoauth",
            useTicket: true,
            crossDomain: false
        }, f);
        h.para = {};
        h.init = function () {
            if (h.inited) {
                return
            }
            h.set_options();
            h.bindListener();
            h.inited = true
        };
        h.set_options = function (i) {
            i = i || {};
            g = c(g, i);
            h.set_sso(i)
        };
        h.set_sso = function (i) {
            i = i || {};
            var j = {};
            j = c(j, g);
            delete j.savestate;
            delete j.vsnf;
            delete j.hold_login_state;
            delete j.cookie_timeout;
            j = c(j, i);
            d.foreach(j, function (l, k) {
                if (l !== e) {
                    a[k] = l
                }
            })
        };
        h.set_extra = function (i) {
            i = i || {};
            if (!a.loginExtraQuery) {
                a.loginExtraQuery = {}
            }
            if (g.cookie_timeout) {
                a.loginExtraQuery.ct = g.cookie_timeout
            }
            a.loginExtraQuery.vsnf = g.vsnf;
            a.loginExtraQuery.s = g.hold_login_state ? 1 : 0;
            a.loginExtraQuery = c(a.loginExtraQuery, i)
        };
        h.login = function (j, l, k, i) {
            k = k || {};
            h.set_sso(k);
            h.para.userid = j;
            h.para.password = l;
            var m = k.savestate || g.savestate;
            if (m) {
                h.para.savestate = m
            }
            a.loginExtraQuery = {};
            h.set_extra(i);
            a.login(h.para.userid, h.para.password, h.para.savestate)
        };
        h.logout = function () {
            a.logout()
        };
        h.verify = function (i, j) {
            if (i == "vsn") {
                h.set_extra({
                    vsnval: j
                })
            } else {
                if (i == "code") {
                    h.set_extra({
                        door: j
                    })
                }
            }
            a.login(h.para.userid, h.para.password, h.para.savestate)
        };
        h.login_callback = function (j) {
            b.fire("login_complete", [j]);
            if (j.result) {
                b.fire("login_success", [j])
            } else {
                var i = {};
                i.code = j.errno;
                i.reason = j.reason;
                var k = d.inArray(i.code, ["5024", "5025", "4049", "2070"]);
                if (k) {
                    b.fire("need_verify", [i])
                } else {
                    b.fire("login_failure", [i])
                }
            }
        };
        h.logout_callback = function (i) {
            b.fire("logout_complete", [i]);
            if (i.result) {
                b.fire("logout_success", [i])
            } else {
                b.fire("logout_failure", [i])
            }
        };
        h.bindListener = function () {
            a.customLoginCallBack = h.login_callback;
            a.customLogoutCallBack = h.logout_callback;
            b.register("login", h.login);
            b.register("verify", h.verify);
            b.register("logout", h.logout)
        };
        return h
    }
});
STK.register("jobs.oauth2.sso.login", function (a) {
    a.jobsM.register("jobs.oauth2.sso.login", function () {
        var b = a.common.util.sso({
            cookie_timeout: 0,
            noActiveTime: 0,
            crossDomain: false,
            entry: "sinaoauth",
            domain: "sina.com.cn",
            service: "sinaoauth"
        });
        b.init()
    })
});
STK.register("kit.extra.language", function (a) {
    var b = window.$LANG || {};
    return function (c, d) {
        var e = a.core.util.language(c, b);
        e = e.replace(/\\}/ig, "}");
        if (d) {
            e = a.templet(e, d)
        }
        return e
    }
});
STK.register("kit.dom.builder", function (b) {
    var a = null;
    return function (c) {
        var d = null;
        if (typeof (c) == "string") {
            if (!a) {
                a = b.C("div")
            }
            a.innerHTML = c;
            d = a.children[0];
            a.removeChild(d);
            a.innerHTML = ""
        } else {
            d = c
        }
        var f = {};
        var e = d.getElementsByTagName("*");
        b.foreach(e, function (i) {
            var h = i.getAttribute("node-type");
            if (h) {
                if (!f[h]) {
                    f[h] = []
                }
                f[h].push(i)
            }
        });
        var g = {};
        g.box = d;
        g.list = f;
        return g
    }
});
STK.register("kit.dom.parseDOM", function (a) {
    return function (c) {
        for (var b in c) {
            if (c[b] && (c[b].length == 1)) {
                c[b] = c[b][0]
            }
        }
        return c
    }
});
STK.register("comp.layer.bubble.relate_tip", function (c) {
    var b = c.core.dom.getSize,
        d = c.kit.dom.builder,
        a = c.kit.dom.parseDOM;
    return function (f) {
        var j = {};
        var i = ['<div class="tips">', '<span node-type="content"></span>', '<button node-type="close" class="close" style="cursor:pointer;">×</button>', "</div>"].join("");
        var g = {
            template: i,
            related_el: null,
            parent_node: document.body,
            direction: "top",
            margin: 0,
            styles: {}
        };
        j.conf = g;
        var e = {
            position: "absolute"
        };
        j.init = function () {
            j.root = null;
            j.nodes = {};
            j.set_options(f)
        };
        j.set_options = function (k) {
            g = c.parseParam(g, k);
            e = c.core.json.merge(e, g.styles)
        };
        j.build = function () {
            var k = d(g.template);
            j.root = k.box;
            j.nodes = a(k.list);
            g.parent_node.appendChild(j.root);
            j.setEvents("add")
        };
        j.set_styles = function (k) {
            k = k || e;
            if (j.root) {
                c.foreach(k, function (m, l) {
                    c.setStyle(j.root, l, m)
                })
            }
        };
        j.show = function (k, l) {
            j.visible = true;
            if (!j.root) {
                j.build()
            }
            j.set_styles();
            if (l) {
                g.related_el = l
            }
            if (j.root && g.related_el) {
                c.setStyle(j.root, "display", "")
            }
            j.set_content(k);
            j.set_position()
        };
        j.set_content = function (l) {
            if (j.nodes) {
                var k = j.nodes.content || j.root;
                if (l) {
                    k.innerHTML = l
                }
            }
        };
        j.get_content = function () {
            if (j.nodes) {
                var k = j.nodes.content || j.root;
                return k.innerHTML
            }
        };
        j.hide = function () {
            j.visible = false;
            if (j.root) {
                c.setStyle(j.root, "display", "none")
            }
        };
        j.set_position = function () {
            var m = g.related_el;
            if (j.root && m) {
                var o = {};
                var p = c.position(m, {
                    parent: g.parent_node
                });
                var l = b(m);
                o.left = p.l;
                o.top = p.t;
                o.right = p.l + l.width;
                o.bottom = p.t + l.height;
                var n = b(j.root);
                var k = {};
                k.top = o.top;
                k.left = o.left;
                if (g.direction == "right") {
                    k.left = o.right + g.margin
                } else {
                    if (g.direction == "bottom") {
                        k.top = o.bottom + g.margin
                    } else {
                        if (g.direction == "left") {
                            k.left = o.left - n.width - g.margin
                        } else {
                            k.top = o.top - n.height - g.margin
                        }
                    }
                }
                c.setStyle(j.root, "top", k.top + "px");
                c.setStyle(j.root, "left", k.left + "px")
            }
        };
        var h = {
            hide: function () {
                c.preventDefault();
                j.hide()
            }
        };
        j.setEvents = function (k) {
            var l = k + "Event";
            c[l](j.nodes.close, "click", h.hide)
        };
        j.destroy = function () {
            j.setEvents("remove");
            if (j.root && j.root.parentNode) {
                j.root.parentNode.removeChild(j.root)
            }
            j.root = null;
            j.nodes = {}
        };
        j.init();
        j.conf = g;
        return j
    }
});
STK.register("common.util.checkcode", function (b) {
    var a = window.sinaSSOController;
    if (a && a.getServerTime) {
        a.getServerTime()
    }
    return function (c) {
        var e = {},
            d = {};
        e.argsCheck = function () {
            d = b.parseParam({
                autofocus: false,
                address: "",
                usesso: false,
                img: null,
                input: null,
                tip: null,
                button: null
            }, c)
        };
        e.init = function () {
            e.argsCheck();
            e.setEvents("add");
            e.change()
        };
        e.change = function () {
            var g = "/aj3/pincode/pin1.php",
                h = b.cookie.get("wvr"),
                i = parseFloat(h, 10);
            if (d.address) {
                g = d.address
            } else {
                if (!isNaN(i) && i && i < 3.6) {
                    g = "/pincode/pin1.php"
                }
            } if (d.tip) {
                d.tip.innerHTML = ""
            }
            if (d.input) {
                d.input.value = "";
                if (d.autofocus) {
                    d.input.focus()
                }
            }
            if (d.img) {
                if (d.usesso && a && a.getPinCodeUrl) {
                    d.img.src = a.getPinCodeUrl()
                } else {
                    d.img.src = g + "?r=" + (new Date() - 0) + "&lang=zh"
                }
            }
        };
        var f = function () {
            b.preventDefault();
            e.change()
        };
        e.setEvents = function (g) {
            var h = g + "Event";
            b[h](d.button, "click", f)
        };
        e.destroy = function () {
            e.setEvents("remove")
        };
        return e
    }
});
STK.register("comp.layer.sso_verify", function (c) {
    var a = c.kit.extra.language,
        i = c.kit.dom.builder,
        f = c.kit.dom.parseDOM,
        e = c.core.json.merge,
        h = c.common.util.checkcode,
        d = c.common.channel.sso,
        b = c.comp.layer.bubble.relate_tip;
    var g = window.sinaSSOController;
    return function (j) {
        var m = ['<div class="W_layer">', '<article class="L_bind_pw" style="position:relative;" node-type="inner">', '<div class="close" node-type="close">×</div>', '<div node-type="vsn_box" style="display:none;">', "<p>#L{T010001}</p>", '<div class="input">', '<input type="text" maxlength="6" name="vsnval" node-type="vsn_input">', "</div>", "</div>", '<div node-type="code_box" style="display:none;">', "<p>#L{T010002}</p>", '<div class="input">', '<input type="text" style=" color:#9a9a9a;" maxlength="5" name="door" node-type="code_input" class="WB_iptxt input_code">', '<span class="code_img">', '<a href="javascript:;" node-type="code_change" title="#L{T010003}">', '<img width="75" height="30" alt="" node-type="code_img">', "</a>", "</span>", "</div>", "</div>", '<div class="btns" style="clear:both;">', '<a class="btnPs" href="javascript:;" node-type="OK">#L{T100002}</a>', '<a class="btnGs" href="javascript:;" node-type="cancel">#L{T100003}</a>', "</div>", "</article>", "</div>"].join("");
        var n = {};
        var k = {
            template: m,
            parent_node: document.body,
            mask_object: null,
            mask_background: "#fff",
            bubble_template: "",
            bubble_margin: 10,
            styles: {
                position: "absolute",
                width: "280px",
                marginLeft: "-150px",
                left: "50%",
                top: "260px"
            }
        };
        n.init = function () {
            k = c.parseParam(k, j);
            n.bindListener()
        };
        n.build = function () {
            var o = a(k.template);
            var q = i(o);
            n.root = q.box;
            n.nodes = f(q.list);
            k.parent_node.appendChild(n.root);
            n.setEvents("add");
            var p = {
                margin: k.bubble_margin,
                parent_node: n.nodes.inner,
                styles: {
                    width: "200px"
                }
            };
            if (k.bubble_template) {
                p.template = k.bubble_template
            }
            n.bubble_tip = b(p)
        };
        n.build_code = function () {
            c.setStyle(n.nodes.vsn_box, "display", "none");
            c.setStyle(n.nodes.code_box, "display", "");
            if (!n.checkcode) {
                n.checkcode = h({
                    usesso: true,
                    img: n.nodes.code_img,
                    input: n.nodes.code_input,
                    tip: null,
                    button: n.nodes.code_change
                });
                n.checkcode.init()
            }
        };
        n.build_vsn = function () {
            c.setStyle(n.nodes.vsn_box, "display", "");
            c.setStyle(n.nodes.code_box, "display", "none")
        };
        n.set_tip = function (q, p) {
            var o = n.bubble_tip;
            if (q && p) {
                if (!o.visible) {
                    o.show(q, p)
                }
            } else {
                o.hide()
            }
        };
        n.hide_tip = function () {
            n.set_tip()
        };
        n.show = function (o) {
            if (!n.root) {
                n.build()
            }
            if (!n.visible) {
                n.set_styles();
                c.setStyle(n.root, "display", "");
                if (k.mask_object) {
                    k.mask_object.showUnderNode(n.root, {
                        useIframeInIE6: false,
                        background: k.mask_background
                    })
                }
                n.type = o == "vsn" ? "vsn" : "code";
                n["build_" + n.type]();
                n.visible = true
            }
        };
        n.set_styles = function (o) {
            o = o || {};
            o = e(k.styles, o);
            if (n.root) {
                c.foreach(o, function (q, p) {
                    c.setStyle(n.root, p, q)
                })
            }
        };
        n.hide = function () {
            c.setStyle(n.root, "display", "none");
            if (k.mask_object) {
                k.mask_object.hide(n.root)
            }
            n.visible = false
        };
        n.check_submit = function () {
            var p = n.type;
            var o = n.nodes[p + "_input"];
            o.value = c.trim(o.value);
            if (o.value) {
                n.submit(p, o.value)
            } else {
                var q = p == "vsn" ? a("#L{E010004}") : a("#L{E010003}");
                n.set_tip(q, o)
            }
        };
        n.submit = function (o, p) {
            if (!g.loginExtraQuery.s) {
                g.appLoginURL["sina.com.cn"] = 1
            }
            d.fire("verify", [o, p]);
            delete g.appLoginURL["sina.com.cn"]
        };
        n.check_login = function (p) {
            var o = null;
            if (p.code == "4049" || p.code == "2070") {
                n.show("code");
                n.checkcode.change();
                o = n.nodes.code_input
            } else {
                n.show("vsn");
                o = n.nodes.vsn_input
            } if (o) {
                o.focus();
                setTimeout(function () {
                    n.set_tip(p.reason, o)
                }, 10)
            }
        };
        var l = {
            hide: function () {
                c.preventDefault();
                n.hide()
            }, check_submit: function () {
                c.preventDefault();
                n.check_submit()
            }
        };
        n.setEvents = function (o) {
            var p = o + "Event";
            c[p](n.nodes.close, "click", l.hide);
            c[p](n.nodes.cancel, "click", l.hide);
            c[p](n.nodes.OK, "click", l.check_submit);
            c[p](n.nodes.code_input, "focus", n.hide_tip);
            c[p](n.nodes.vsn_input, "focus", n.hide_tip)
        };
        n.bindListener = function () {
            d.register("need_verify", n.check_login);
            d.register("login_success", n.hide)
        };
        n.destroy = function () {
            n.setEvents("remove");
            n.bubble_tip.destroy()
        };
        return n
    }
});
STK.register("kit.dom.cssText", function (b) {
    var a = function (f, e) {
        var c = (f + ";" + e).replace(/(\s*(;)\s*)|(\s*(:)\s*)/g, "$2$4"),
            d;
        while (c && (d = c.match(/(^|;)([\w\-]+:)([^;]*);(.*;)?\2/i))) {
            c = c.replace(d[1] + d[2] + d[3], "")
        }
        return c
    };
    return function (d) {
        d = d || "";
        var e = [],
            c = {
                push: function (g, f) {
                    e.push(g + ":" + f);
                    return c
                }, remove: function (g) {
                    for (var f = 0; f < e.length; f++) {
                        if (e[f].indexOf(g + ":") == 0) {
                            e.splice(f, 1)
                        }
                    }
                    return c
                }, getStyleList: function () {
                    return e.slice()
                }, getCss: function () {
                    return a(d, e.join(";"))
                }
            };
        return c
    }
});
STK.register("kit.dom.fix", function (d) {
    var a = !(d.core.util.browser.IE6 || (document.compatMode !== "CSS1Compat" && STK.IE)),
        b = /^(c)|(lt)|(lb)|(rt)|(rb)$/;

    function c(g) {
        return d.core.dom.getStyle(g, "display") != "none"
    }

    function e(h) {
        h = d.core.arr.isArray(h) ? h : [0, 0];
        for (var g = 0; g < 2; g++) {
            if (typeof h[g] != "number") {
                h[g] = 0
            }
        }
        return h
    }

    function f(j, r, m) {
        if (!c(j)) {
            return
        }
        var q = "fixed",
            t, u, g, p, k = j.offsetWidth,f
            l = j.offsetHeight,
            n = d.core.util.winSize(),
            o = 0,
            s = 0,
            h = d.kit.dom.cssText(j.style.cssText);
        if (!a) {
            q = "absolute";
            var i = d.core.util.scrollPos();
            o = t = i.top;
            s = u = i.left;
            switch (r) {
            case "lt":
                t += m[1];
                u += m[0];
                break;
            case "lb":
                t += n.height - l - m[1];
                u += m[0];
                break;
            case "rt":
                t += m[1];
                u += n.width - k - m[0];
                break;
            case "rb":
                t += n.height - l - m[1];
                u += n.width - k - m[0];
                break;
            case "c":
            default:
                t += (n.height - l) / 2 + m[1];
                u += (n.width - k) / 2 + m[0]
            }
            g = p = ""
        } else {
            t = p = m[1];
            u = g = m[0];
            switch (r) {
            case "lt":
                p = g = "";
                break;
            case "lb":
                t = g = "";
                break;
            case "rt":
                u = p = "";
                break;
            case "rb":
                t = u = "";
                break;
            case "c":
            default:
                t = (n.height - l) / 2 + m[1];
                u = (n.width - k) / 2 + m[0];
                p = g = ""
            }
        } if (r == "c") {
            if (t < o) {
                t = o
            }
            if (u < s) {
                u = s
            }
        }
        h.push("position", q).push("top", t + "px").push("left", u + "px").push("right", g + "px").push("bottom", p + "px");
        j.style.cssText = h.getCss()
    }
    return function (h, n, i) {
        var j, o, k = true,
            g;
        if (d.core.dom.isNode(h) && b.test(n)) {
            var l = {
                getNode: function () {
                    return h
                }, isFixed: function () {
                    return k
                }, setFixed: function (p) {
                    (k = !!p) && f(h, j, o);
                    return this
                }, setAlign: function (p, q) {
                    if (b.test(p)) {
                        j = p;
                        o = e(q);
                        k && f(h, j, o)
                    }
                    return this
                }, destroy: function () {
                    if (!a) {
                        a && d.core.evt.removeEvent(window, "scroll", m)
                    }
                    d.core.evt.removeEvent(window, "resize", m);
                    d.core.evt.custEvent.undefine(g)
                }
            };
            g = d.core.evt.custEvent.define(l, "beforeFix");
            l.setAlign(n, i);

            function m(p) {
                p = p || window.event;
                d.core.evt.custEvent.fire(g, "beforeFix", p.type);
                if (k && (!a || j == "c")) {
                    f(h, j, o)
                }
            }
            if (!a) {
                d.core.evt.addEvent(window, "scroll", m)
            }
            d.core.evt.addEvent(window, "resize", m);
            return l
        }
    }
});
STK.register("module.mask", function (e) {
    var l, c = [],
        h, m, d;
    var g = e.core.dom.setStyle;
    var j = e.core.dom.getStyle;
    var k = e.core.evt.custEvent;
    var b = {},
        a;

    function i(o) {
        l = e.C("div");
        var n = '<div node-type="outer">';
        if (e.core.util.browser.IE6 && o.useIframeInIE6) {
            n += '<iframe style="position:absolute;z-index:-1;width:100%;height:100%;filter:mask();"></iframe>'
        }
        n += "</div>";
        l = e.builder(n).list.outer[0];
        document.body.appendChild(l);
        m = true;
        h = e.kit.dom.fix(l, "lt");
        var p = function () {
            var q = e.core.util.winSize();
            l.style.cssText = e.kit.dom.cssText(l.style.cssText).push("width", q.width + "px").push("height", q.height + "px").getCss()
        };
        d = k.add(h, "beforeFix", p);
        p()
    }
    var f = {
        getNode: function () {
            return l
        }, show: function (o, n) {
            if (m) {
                o = e.core.obj.parseParam({
                    useIframeInIE6: true,
                    opacity: 0.1,
                    background: "#000000"
                }, o);
                l.style.background = o.background;
                g(l, "opacity", o.opacity);
                l.style.display = "block";
                h.setAlign("lt");
                n && n()
            } else {
                e.Ready(function () {
                    i(o);
                    f.show(o, n)
                })
            }
            return f
        }, hide: function (p) {
            if (l && p) {
                if (a != p) {
                    delete b[e.core.dom.uniqueID(p)]
                } else {
                    var q = e.core.dom.prev(l);
                    if (a) {
                        delete b[e.core.dom.uniqueID(a)];
                        a = undefined
                    }
                    var o = false;
                    for (var n = 0; q && n < 3; n++) {
                        if (b[e.core.dom.uniqueID(q)]) {
                            o = true;
                            break
                        }
                        q = e.core.dom.prev(q)
                    }
                    if (o) {
                        f.showUnderNode(q)
                    } else {
                        l.style.display = "none"
                    }
                    q = undefined
                }
            }
            p = undefined;
            return f
        }, showUnderNode: function (o, n) {
            if (e.isNode(o)) {
                (a = o);
                b[e.core.dom.uniqueID(o)] = 1;
                f.show(n, function () {
                    document.body.appendChild(l);
                    document.body.appendChild(o);
                    g(l, "zIndex", j(o, "zIndex"))
                })
            }
            return f
        }, destroy: function () {
            k.remove(d);
            l.style.display = "none";
            a = undefined;
            b = {}
        }
    };
    return f
});
STK.register("jobs.oauth2.sso.verify", function (a) {
    var b = a.module.mask;
    a.jobsM.register("jobs.oauth2.sso.verify", function () {
        var d = ['<div class="WB_tips_yls">', '<span class="WB_tipS_err"></span>', '<span class="WB_sp_txt" node-type="content"></span>', '<span class="arr"></span>', "</div>"].join("");
        var e = ['<div class="WB_dialog">', '<div class="WB_panel">', '<div class="input_box1" style="position:relative;" node-type="inner">', '<a class="oauth_layer_close" href="javascript:;" node-type="close"></a>', '<dl class="oauth_layer_form clearfix" node-type="vsn_box" style="display:none;">', '<dt><span class="oauth_icon icon_shield"></span>#L{T010001}</dt>', '<dd><input type="text" maxlength="6" style="color:#9a9a9a;" class="WB_iptxt" name="vsnval" node-type="vsn_input"></dd>', "</dl>", '<dl class="oauth_layer_form layer_form02 clearfix" node-type="code_box" style="display:none;">', '<dt><span class="oauth_icon icon_shield"></span>#L{T010002}</dt>', "<dd>", '<input type="text" maxlength="5" style="color:#9a9a9a;" class="WB_iptxt input_code" name="door" node-type="code_input">', '<span class="code_img">', '<img width="75" height="30" alt="" node-type="code_img">', "</span>", '<a class="code_change" href="javascript:;" node-type="code_change">#L{T010003}</a>', "</dd>", "</dl>", '<p class="oauth_layer_formbtn">', '<a class="WB_btnA" href="javascript:;" node-type="OK"><span>#L{T100002}</span></a>', '<a class="WB_btnB" href="javascript:;" node-type="cancel"><span>#L{T100003}</span></a>', "</p>", "</div>", "</div>", "</div>"].join("");
        var c = a.comp.layer.sso_verify({
            template: e,
            bubble_template: d,
            bubble_margin: 12,
            mask_object: b,
            styles: {
                position: "absolute",
                width: "327px",
                marginLeft: "-172px",
                left: "50%",
                top: "80px"
            }
        });
        c.init()
    })
});
STK.register("kit.dom.htmlToJson", function (a) {
    return function (d) {
        var f = {};
        var b = d.getElementsByTagName("*");
        var e = function (j) {
            var h = j.getAttribute("name");
            var i = j.getAttribute("type");
            var g = true;
            if (i == "checkbox" || i == "radio") {
                g = j.checked
            }
            if (h && g) {
                f[h] = j.value
            }
        };
        for (var c = 0; c < b.length; c++) {
            e(b[c])
        }
        return f
    }
});
STK.register("comp.oauth2.authorize", function (f) {
    var d = f.kit.extra.language,
        h = f.kit.dom.builder,
        c = f.kit.dom.parseDOM,
        b = f.kit.dom.htmlToJson,
        g = f.comp.layer.bubble.relate_tip,
        e = f.common.channel.sso;
    var a = window.sinaSSOController;
    return function (k, t) {
        var o = {},
            p = {
                bubble_template: "",
                bubble_margin: 10
            };
        var n = {
            objs: {},
            nodes: {},
            domEventFuns: {
                check_userid_keydown: function (v) {
                    v = f.fixEvent(v);
                    if (v.keyCode == 13) {
                        if (n.nodes.password.value) {
                            n.submit()
                        } else {
                            n.nodes.password.focus()
                        }
                    } else {
                        if (v.keyCode == 9) {
                            setTimeout(function () {
                                n.nodes.password.focus()
                            }, 10)
                        }
                    }
                }, check_password_keydown: function (v) {
                    v = f.fixEvent(v);
                    if (v.keyCode == 13) {
                        if (n.nodes.userid.value) {
                            n.submit()
                        } else {
                            n.nodes.userid.focus()
                        }
                    }
                }, submit: function () {
                    f.preventDefault();
                    n.submit()
                }, change_account: function () {
                    f.preventDefault();
                    e.fire("logout")
                }, hide_tip: function () {
                    n.set_tip()
                }
            },
            custEventFuns: {},
            listenerFuns: {
                login_success: function (y) {
                    if (n.nodes.login_weibo && n.nodes.login_weibo.checked) {
                        var A = n.get_data();
                        delete A.userid;
                        delete A.password;
                        delete A.login_weibo;
                        if (y.ticket) {
                            A.ticket = y.ticket
                        }
                        A.redirect_uri = encodeURIComponent(A.redirect_uri);
                        var z = f.jsonToQuery(A);
                        var v = window.location.href.split("?")[0] + "?" + z;
                        var x = "http://login.sina.com.cn/crossdomain2.php?action=login&r=" + encodeURIComponent(v);
                        window.location.replace(x)
                    } else {
                        if (y.ticket) {
                            var w = f.C("input");
                            w.name = "ticket";
                            w.type = "hidden";
                            w.value = y.ticket;
                            n.nodes.form.appendChild(w)
                        }
                        n.nodes.form.submit()
                    }
                }, login_failure: function (v) {
                    v = v || {};
                    var w = v.reason || d("#L{E010005}");
                    n.set_tip(w)
                }, logout_success: function () {
                    var v = n.get_method();
                    if (v == "post") {
                        n.nodes.form.submit()
                    } else {
                        window.location.reload()
                    }
                }
            },
            get_method: function () {
                var v = "get";
                if (window.$CONFIG) {
                    v = $CONFIG.logout_method;
                    if (v) {
                        v = v.toString().toLowerCase()
                    }
                }
                return v
            }, get_data: function () {
                var v = n.nodes.userid;
                if (v) {
                    v.value = f.trim(v.value)
                }
                return b(k)
            }, validate: function () {
                var w = n.get_data();
                var v = true;
                if (n.nodes.userid && !w.userid) {
                    n.set_tip(d("#L{E010001}"), n.nodes.userid);
                    v = false
                }
                if (n.nodes.password && !w.password) {
                    n.set_tip(d("#L{E010002}"), n.nodes.password);
                    v = false
                }
                return v
            }, submit: function () {
                if (n.validate()) {
                    var w = n.get_data();
                    if (n.nodes.userid && n.nodes.password) {
                        var v = {};
                        v.crossDomain = false;
                        if (w.login_weibo) {
                            v.hold_login_state = true;
                            v.cookie_timeout = 1800
                        } else {
                            a.appLoginURL["sina.com.cn"] = 1;
                            v.hold_login_state = false;
                            v.cookie_timeout = 0
                        }
                        e.fire("login", [w.userid, w.password, v]);
                        delete a.appLoginURL["sina.com.cn"]
                    } else {
                        if (n.nodes.form) {
                            n.nodes.form.submit()
                        }
                    }
                }
            }, set_tip: function (x, w) {
                var v = n.objs.bubble_tip;
                w = w || n.nodes.userid;
                if (x && w) {
                    if (!v.visible) {
                        v.show(x, w)
                    }
                } else {
                    v.hide()
                }
            }
        };
        var q = function () {
            if (!k) {
                throw "STK.comp.oauth2.authorize : node is not a Node !"
            }
            p = f.parseParam(p, t)
        };
        var j = function () {
            n.nodes = c(h(k).list)
        };
        var l = function () {
            var v = {
                margin: p.bubble_margin,
                parent_node: k,
                styles: {
                    width: "200px"
                }
            };
            if (p.bubble_template) {
                v.template = p.bubble_template
            }
            n.objs.bubble_tip = g(v)
        };
        var m = function () {
            f.addEvent(n.nodes.submit, "click", n.domEventFuns.submit);
            f.addEvent(n.nodes.userid, "keydown", n.domEventFuns.check_userid_keydown);
            f.addEvent(n.nodes.password, "keydown", n.domEventFuns.check_password_keydown);
            f.addEvent(n.nodes.userid, "focus", n.domEventFuns.hide_tip);
            f.addEvent(n.nodes.password, "focus", n.domEventFuns.hide_tip);
            f.addEvent(n.nodes.change_account, "click", n.domEventFuns.change_account)
        };
        var i = function () {};
        var r = function () {
            e.register("login_success", n.listenerFuns.login_success);
            e.register("login_failure", n.listenerFuns.login_failure);
            e.register("logout_success", n.listenerFuns.logout_success)
        };
        var s = function () {
            if (n) {
                f.foreach(n.objs, function (v) {
                    if (v.destroy) {
                        v.destroy()
                    }
                });
                n = null
            }
        };
        var u = function () {
            q();
            j();
            l();
            m();
            i();
            r()
        };
        u();
        o.nodes = n.nodes;
        o.submit = n.submit;
        o.destroy = s;
        return o
    }
});
STK.register("kit.dom.placeholder", function (c) {
    var b = c.core.json.merge;
    var a = "placeholder" in c.C("input");
    return function (g, d) {
        var f = {};
        var e = c.parseParam({}, d);
        var h = {
            opacity: 0.5
        };
        f.compute_offset = function () {
            var i = {};
            c.foreach(["marginTop", "paddingTop", "borderTopWidth", "marginLeft", "paddingLeft", "borderLeftWidth"], function (j) {
                i[j] = c.getStyle(g, j);
                if (i[j] == "auto") {
                    i[j] = "1px"
                }
                i[j] = parseInt(i[j], 10) || 0
            });
            i.x = i.marginLeft + i.paddingLeft + i.borderLeftWidth;
            i.y = i.marginTop + i.paddingTop + i.borderTopWidth + (c.core.util.browser.IE6 ? 1 : 0);
            return i
        };
        f.getStyles = function () {
            var i = {};
            c.foreach(["fontSize", "lineHeight"], function (j) {
                i[j] = c.getStyle(g, j)
            });
            i.position = "absolute";
            return i
        };
        f.focus = function () {
            f.hide();
            setTimeout(function () {
                g.focus()
            })
        };
        f.hide = function () {
            c.setStyle(f.label, "display", "none")
        };
        f.show = function () {
            if (!g.value) {
                c.setStyle(f.label, "display", "")
            }
        };
        f.build_placeholder = function (k) {
            if (!f.label) {
                f.label = c.C("label");
                f.hide();
                c.insertBefore(f.label, g);
                f.bindDomEvents()
            }
            f.label.innerHTML = k;
            var i = f.getStyles();
            var j = f.compute_offset();
            i.marginLeft = j.x + "px";
            i.marginTop = j.y + "px";
            i = b(i, h);
            c.foreach(i, function (m, l) {
                c.setStyle(f.label, l, m)
            })
        };
        f.bindDomEvents = function () {
            c.addEvent(g, "input", f.hide);
            c.addEvent(g, "propertychange", f.hide);
            c.addEvent(g, "focus", f.hide);
            c.addEvent(g, "blur", f.show);
            c.addEvent(f.label, "mousedown", f.focus)
        };
        f.destroy = function () {
            c.removeEvent(g, "focus", f.hide);
            c.removeEvent(f.label, "mousedown", f.focus);
            c.removeEvent(g, "blur", f.show);
            if (f.label && f.label.parentNode) {
                f.label.parentNode.removeChild(f.label)
            }
            f.label = null
        };
        f.set = function (j, i) {
            if (!g) {
                return
            }
            i = i || {};
            h = b({
                color: "#888"
            }, i);
            if (!j) {
                j = g.getAttribute("placeholder") || ""
            }
            if (a) {
                g.setAttribute("placeholder", j)
            } else {
                f.build_placeholder(j);
                if (g.value) {
                    f.hide()
                } else {
                    f.show()
                }
            }
            return f
        };
        f.node = g;
        f.conf = e;
        f.conf_style = h;
        return f
    }
});
STK.register("jobs.oauth2.authorize", function (b) {
    var a = b.kit.dom.placeholder;
    b.jobsM.register("jobs.oauth2.authorize", function () {
        var e = b.E("authz_form");
        b.setStyle(e, "position", "relative");
        var c = ['<div class="WB_tips_yls">', '<span class="WB_tipS_err"></span>', '<span class="WB_sp_txt" node-type="content"></span>', '<span class="arr"></span>', "</div>"].join("");
        var d = b.comp.oauth2.authorize(e, {
            bubble_template: c,
            bubble_margin: 12
        });
        a(d.nodes.userid).set()
    })
});