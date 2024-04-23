import React, { useEffect, useState, useRef } from "react";

import Editor, { useMonaco } from "@monaco-editor/react";
import "monaco-themes/themes/Blackboard.json";
import "monaco-themes/themes/Night Owl.json";
import "monaco-themes/themes/Tomorrow-Night-Blue.json";



const Main = () => {
  const monaco = useMonaco();
  const [activeTab, setActiveTab] = useState(0);
  const [code, setCode] = useState("# Here is your python module");
  const [command, setCommand] = useState("");
  const [theme, setTheme] = useState("Merbivore");
  const [language, setSelectedLanguage] = useState('python');
  const [tabs, setTabs] = useState([
    {
      id: 0,
      title: "main.py",
      created: new Date(),
      modified: new Date(),
      code: "\n# ██╗░░░██╗██████╗░██╗░░░░░██╗██████╗░███████╗\n# ██║░░░██║██╔══██╗██║░░░░░██║██╔══██╗██╔════╝\n# ╚██╗░██╔╝██████╔╝██║░░░░░██║██║░░██║█████╗░░\n# ░╚████╔╝░██╔═══╝░██║░░░░░██║██║░░██║██╔══╝░░\n# ░░╚██╔╝░░██║░░░░░███████╗██║██████╔╝███████╗\n# ░░░╚═╝░░░╚═╝░░░░░╚══════╝╚═╝╚═════╝░╚══════╝\n\ndef main():\n\tprint('<-- Hello World! -->')\n\treturn 0\n\nif __name__==\"__main__\":\n\tmain()\n\n",
    },
  ]);
  const [txt, setTxt] = useState("");
  const [wsocket, setWsocket] = useState(null);

  const initialRender = useRef(true);
  const initialRender2 = useRef(true);
  const changeTab = useRef(false);
  const monthNames = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];
  const [newTabTitle, setNewTabTitle] = useState("");

  function handleCommandChange(e) {
    setCommand(e.target.value);
  }

  function handleSendCommand(e) {
    if (e.key === 'Enter') {
      e.preventDefault()
      let result_text = "";
      let shellCommand = command.trim()
      if (shellCommand == "ls") {
        tabs.forEach((e) => {
          result_text = result_text.concat(`${e.title}\t`)
        });
      } else if (shellCommand == "ls -l") {
        tabs.forEach((e) => {
          const dummy_date = new Date();
          const full_time = e.modified.getFullYear() === dummy_date.getFullYear() ? e.modified.getHours() + ":" + e.modified.getMinutes() + ":" + e.modified.getSeconds() : e.modified.getFullYear();
          result_text = result_text.concat(`${monthNames[e.modified.getMonth()]}  ${e.modified.getDay()}  ${full_time}  ${e.title}\n`)
        });
      } else if (shellCommand.startsWith("touch")) {
        setNewTabTitle(shellCommand.split(" ")[1]);
      } else if (wsocket != null) {
        let message = JSON.stringify({
          'command': `${shellCommand}\n`
        })
        wsocket.send(message);
      } 
      else {
        result_text = `> ${shellCommand}: command not found`;
      }
      setTxt(txt.concat("> " + shellCommand + "\n" + result_text + "\n"));
      setCommand("");
    } else;
  }

  const handleAddTab = () => {
    setActiveTab(tabs.length);
  };
  useEffect(() => {
    if (monaco) {
      import('monaco-themes/themes/Merbivore.json')
        .then(data => {
          monaco.editor.defineTheme('merbivore', data);
        })
        .then(_ => monaco.editor.setTheme('merbivore'))
    }
  }, [monaco]);

  const onChange = (e) => {
    tabs[activeTab].code = e;
  };

  const changeTheme = (e) => {
    setTheme(e.target.innerHTML);
    let updatedTheme = e.target.innerHTML;
    import(`monaco-themes/themes/${updatedTheme}.json`)
      .then(data => {
        monaco.editor.defineTheme(updatedTheme.toLowerCase(), data);
      })
      .then(_ => monaco.editor.setTheme(updatedTheme.toLowerCase()))
    const outputW = document.getElementsByClassName("outputWindow")[0];
    let owColor = null;
    switch (updatedTheme.toLowerCase()) {
      case "blackboard":
        owColor = "#0c1021"
        break;
      case "dracula":
        owColor = "#282a36"
        break;
      case "amy":
        owColor = "#200020"
        break;
      case "solarized-dark":
        owColor = "#002B36"
        break;
      case "krtheme":
        owColor = "#0B0A09"
        break;
      case "cobalt":
        owColor = "#082444"
        break;
      case "cobalt2":
        owColor = "#193549"
        break;
      case "merbivore":
        owColor = "#161616"
        break;
      case "monokai":
        owColor = "#272822"
        break;
      case "idlefingers":
        owColor = "#323232"
        break;
      case "monoindustrial":
        owColor = "#222C28"
        break;
      case "nord":
        owColor = "#2E3440"
        break;
      case "spacecadet":
        owColor = "#0D0D0D"
        break;
      case "sunburst":
        owColor = "#000000"
        break;
      case "tomorrow-night":
        owColor = "#1D1F21"
        break;
      case "twilight":
        owColor = "#141414"
        break;
      case "zenburnesque":
        owColor = "#404040"
        break;
      default:
        owColor = "#000"
        break;
    }
    outputW.style["background-color"] = owColor
  }

  const handleClear = (e) => {
    e.preventDefault();
    setTxt(" ");
  }

  const handleSave = (e) => {
    e.preventDefault();
    fetch(`${process.env.REACT_APP_BASE_URL + '/git/commit/'}`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(tabs[activeTab].code),
    }).then((response) => {
      if (response.status !== 200) {
        throw new Error(response.statusText);
      }
      return response.json();
    }).then((response) => {
      console.log(response);

    }).catch((err) => {
      console.log(err);
    })
  };

  function handleEvaluateScripts(e) {
    e.preventDefault();
    const files = tabs.map((tab, index) => {
      var blob = new Blob([JSON.stringify(tab.code, null, 2)], { type: "text/plain" });
      return new File([blob], tab.title, {
        type: blob.type,
      });
    });

    const formData = new FormData();
    files.forEach((file, index) => {
      formData.append(file.name, file);
    });
    formData.append("pl_language", language);

    fetch(`${process.env.REACT_APP_BASE_URL + '/api/evaluate_scripts/'}`, {
      method: "POST",
      body: formData,
    }).then((response) => {
      if (response.status !== 200) {
        throw new Error(response.statusText);
      }
      return response.json();
    }).then((response) => {
      setTxt(txt.concat(response["content"]));
    }).catch((err) => {
      console.log(err);
    })
  }

  const handleEvaluate = (e) => {
    e.preventDefault();
    const files = tabs.map((tab, index) => {
      var blob = new Blob([JSON.stringify(tab.code, null, 2)], { type: "text/plain" });
      return new File([blob], tab.title, {
        type: blob.type,
      });
    });

    const formData = new FormData();
    files.forEach((file, index) => {
      formData.append(file.name, file);
    });
    formData.append("pl_language", language);

    fetch(`${process.env.REACT_APP_BASE_URL + '/api/evaluate/'}`, {
      method: "POST",
      body: formData,
    }).then((response) => {
      if (response.status !== 200) {
        throw new Error(response.statusText);
      }
      return response.json();
    }).then((response) => {
      console.log(response);
      setTxt(txt.concat(response["content"]));
    }).catch((err) => {
      console.log(err);
    })
  };

  const handleDebugMode = (e) => {
    e.preventDefault();
    if (e.target.id === "debug_open") {
      try {
        let socket = new WebSocket(`ws://localhost:8001/ws/execution_debugger/${language}/`);
        setWsocket(socket);
        document.getElementById("debug_open").classList.add("Disabled");
        const debug_buttons = document.getElementsByClassName("debug_process");
        Array.from(debug_buttons).forEach((btn) => {
          btn.classList.remove("Disabled");
        });

        socket.onopen = () => {
          console.log('WebSocket connected');
          const files = tabs.map((tab) => ({
            name: tab.title,
            content: tab.title === "main.py" ? `${tab.code}` : tab.code,
          }));
          socket.send(JSON.stringify({ files }));
        };

        socket.onmessage = (event) => {
          const message = event.data;
          //console.log("Received message:", message);
          var msg = JSON.parse(message).message;
          setTxt(prevTxt => prevTxt + 'Debugger: ' + msg + '\n');
        };

        socket.onclose = () => {
          document.getElementById("debug_open").classList.remove("Disabled");
          const debug_buttons = document.getElementsByClassName("debug_process");
          Array.from(debug_buttons).forEach((btn) => {
            btn.classList.add("Disabled");
          });
          setWsocket(null);
          console.log('Websocket closed');
        };
      } catch (error) {
        console.error(error);
      }
    } else if (e.target.id === "debug_close") {
      document.getElementById("debug_open").classList.remove("Disabled");
      const debug_buttons = document.getElementsByClassName("debug_process");
      Array.from(debug_buttons).forEach((btn) => {
        btn.classList.add("Disabled");
      });
      wsocket.close();
      setWsocket(null);
    }
  };

  const handleStepIn = (e) => {
    var command = {'python': 'next\n', 'cpp': 'next\n', 'c': 'next\n'};
    let message = JSON.stringify({
      'command': command[`${language}`]
    })
    wsocket.send(message);
  };
  const handleStepOut = (e) => {
    var command = {'python': 'return\n', 'cpp': 'return\n', 'c': 'return\n'};
    let message = JSON.stringify({
      'command': command[`${language}`]
    })
    wsocket.send(message);
  };

  const handleStepOver = (e) => {
    var command = {'python': 'step\n', 'cpp': 'step\n', 'c': 'step\n'};
    let message = JSON.stringify({
      'command': command[`${language}`]
    })
    wsocket.send(message);
  };

  const tabOnClick = (e) => {
    const tabNav = Array.prototype.slice.call(document.getElementsByClassName("tabNav")[0].children);
    const indexClicked = tabNav.indexOf(e.target);
    const prevActive = document.getElementsByClassName("tabActive")[0];
    prevActive.classList.remove("tabActive");
    e.target.classList.add("tabActive");
    changeTab.current = true;
    setActiveTab(indexClicked);
  };


  useEffect(() => {
    document.title = 'VPL IDE';
  }, []);


  useEffect(() => {
    if (changeTab.current === true) {
      setCode(tabs[activeTab].code);
      changeTab.current = false;
      return;
    }
    if (initialRender.current === true) {
      initialRender.current = false;
    } else {
      const newTab = {
        id: tabs.length,
        title: newTabTitle || `tab${tabs.length}.py`,
        modified: new Date(),
        created: new Date(),
        code: newTabTitle ? `# New tab named ${newTabTitle}` : `# New tab named newtab${tabs.length}.py`,
      };
      initialRender2.current = true;
      setNewTabTitle("");
      setTabs([...tabs, newTab]);
    }
  }, [activeTab]);

  useEffect(() => {
    if (initialRender2.current === true) {
      initialRender2.current = false;
    } else {
      handleAddTab();
    }
  }, [newTabTitle]);


  useEffect(() => {
    const tabNav = document.getElementsByClassName("tabNav")[0];
    const lastTab = tabs[activeTab];
    const activeTabbb = document.getElementsByClassName("tabActive")[0];
    if (activeTabbb) {
      activeTabbb.classList.remove("tabActive");
    }

    const newTab = document.createElement("input");
    newTab.type = "button"
    newTab.value = lastTab.title;
    newTab.classList.add("tabActive");
    newTab.classList.add("tabCommon");
    newTab.onclick = tabOnClick;
    tabNav.appendChild(newTab);
    setCode(lastTab.code);
  }, [tabs]);

  
    const handleLanguageChange = (event) => {
      setSelectedLanguage(event.target.innerHTML);
    };
  
  return (
    <>
      <div className='navbar'>
        <div>
          <img src="/vplide_trans.png" alt="VPLIDE" className="vplideLogo" />
        </div>
        <label className="dropdown">
          Theme:
          <div className="dd-button">
            {theme}
          </div>
          <input type="checkbox" className="dd-input" id="test" />
          <ul className="dd-menu">
            <li onClick={changeTheme}>Blackboard</li>
            <li onClick={changeTheme}>Dracula</li>
            <li onClick={changeTheme}>Amy</li>
            <li onClick={changeTheme}>Solarized-dark</li>
            <li onClick={changeTheme}>krTheme</li>
            <li onClick={changeTheme}>Cobalt</li>
            <li onClick={changeTheme}>Cobalt2</li>
            <li onClick={changeTheme}>Merbivore</li>
            <li onClick={changeTheme}>Monokai</li>
            <li onClick={changeTheme}>idleFingers</li>
            <li onClick={changeTheme}>monoindustrial</li>
            <li onClick={changeTheme}>Nord</li>
            <li onClick={changeTheme}>SpaceCadet</li>
            <li onClick={changeTheme}>Sunburst</li>
            <li onClick={changeTheme}>Tomorrow-Night</li>
            <li onClick={changeTheme}>Twilight</li>
            <li onClick={changeTheme}>Zenburnesque</li>
          </ul>
        </label>
        <label className="dropdown">
          <label className="aa">
            Language:
            <div className="dd-button">
              {language}
            </div>
            <input type="checkbox" className="dd-input" id="test" />
            <ul className="dd-menu">
              <li onClick={handleLanguageChange}>python</li>
              <li onClick={handleLanguageChange}>c</li>
              <li onClick={handleLanguageChange}>cpp</li>
              <li onClick={handleLanguageChange}>java</li>
            </ul>
          </label>
        </label>
      </div>
      <div className="editorField">
        <div className="actionButtons">
          <button className="EditorButton">
            <img src="/run.png" alt="Run" onClick={handleEvaluate} className="EditorImage" />
          </button>
          <button className="EditorButton">
            <img src="/save.png" alt="Run" onClick={handleSave} className="EditorImage" />
          </button>

          <button className="EditorButton" >
            <img src="/debug.png" alt="Run" onClick={handleDebugMode} id="debug_open" className="EditorImage" />
          </button>
          <button className="EditorButton">
            <img src="/step_into.png" alt="Step Into" onClick={handleStepIn} className="EditorImage debug_process Disabled" />
          </button>
          <button className="EditorButton">
            <img src="/step_out.png" alt="Step Out" onClick={handleStepOut} className="EditorImage debug_process Disabled" />
          </button>
          <button className="EditorButton">
            <img src="/step_over.png" alt="Step Over" onClick={handleStepOver} className="EditorImage debug_process Disabled" />
          </button>
          <button className="EditorButton debug_process Disabled">
            <img src="/stop.png" alt="Step Over" onClick={handleDebugMode} id="debug_close" className="EditorImage" />
          </button>
        </div>
        <div className="tabsEditor">
          <div className="tabsWrapper">
            <div className="tabNav" />
            <input onClick={handleAddTab} id="addTabButton" className="addTabButton" type="button" value="+" />
          </div>
          <div className="codeField">
            <Editor
              language={language}
              value={code}
              theme={monaco}
              onChange={onChange}
            />
          </div>
        </div>
      </div>
      <div className="shellField">
        <div className="shellNav">
          <div>
            Shell
          </div>
          <button onClick={handleEvaluateScripts} className="shellButton">Evaluate</button>
          <input onClick={handleClear} className="shellButton" type="button" value="Clear" />
        </div>
        <div className="outputWindow">
          {txt}
          <form>
            {'>'}<input type="text" className="noStyleInput" onKeyDown={handleSendCommand} onChange={handleCommandChange} value={command} />
          </form>
        </div>
      </div>
    </>
  );
};

export default Main;
