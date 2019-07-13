// pages/bubble/bubble.js

var index = require('../../data/data_index.js').index2;
const app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    voiceInput: false,
    queAndAns: [],
    queAndAnsLength: 0,
    totalHeight: 0,
    queText: '',
    ansText: '',
    query: null,
    textInput: '',
    socketTask: null,
    barHeight: 120,
    code: "",
    textareaShow: false,
    textShow: false,
    isSpeaking: false,
    speakAnswer: true,
    openId: "",
    historyNum: 0,
    textareaWidth: 40,
    curQueViewId:'curQueView'
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    var that = this;
    this.getData();
    console.log(this.data.queAndAns);
    wx.getSystemInfo({
      success: function(res) {
        var heightPx = res.windowHeight;
        var widthPx = res.windowWidth;
        var heightRpx = heightPx * 750 / widthPx;
        console.log(widthPx);
        console.log(heightPx);
        console.log(heightRpx);
        that.setData({
          totalHeight: heightRpx
        });
      },
    })
    var query = this.createSelectorQuery();
    this.setData({
      'query': query
    })

    wx.request({
      url: "http://192.168.1.100:8000/index",
      success: function(res) {
        console.log("Chance! Chance!");
        console.log(res.data);
      }
    })

    // wx.setNavigationBarTitle({
    //   "title":""
    // })
    this.setData({
      barHeight: app.globalData.height
    })

    // 本机
    // var url = 'ws://127.0.0.1:8000/echo';
    // 腾讯云服务器
    // var url = 'wss://129.204.225.110:8000/echo';
    // 局域网本机
    var url = 'ws://192.168.1.100:8000/echo';
    // var url = 'ws://192.168.1.107:8000/echo';
    //局域网白云鹏主机
    // var url = 'ws://192.168.43.63:8000/echo';

    var socketTask = wx.connectSocket({
      url: url,
      header: {
        'content-type': 'application/json;charset=utf-8'
        // "content-type": "application/x-www-form-urlencoded;charset=utf-8"
      },
      success: function() {
        console.log('信道连接成功~')
      },
      fail: function() {
        console.log('信道连接失败~')
      }
    })
    this.setData({
      'socketTask': socketTask
    })
    console.log(this.data.socketTask);

    wx.onSocketOpen(function() {
      console.log("have opened! Do what you can!")
    })

    wx.onSocketMessage(function(res) {
      console.log(res.data);
      var reply = JSON.parse(res.data);
      console.log("Server return this:" + reply);
      switch (reply.type) {
        case "text":
          switch (reply.method) {
            case "add":
              that.addAnsAndShow(reply.data);
              break;
            case "reset":
              that.resetText(reply.data);
              break;
          }
          break;
      }

    })

    app.globalData.recoManager.onRecognize = function(res) {
      console.log(res);
      that.setData({
        'queText': res.result,
        'textareaWidth': res.result.length * 36,
      })
      if (that.data.queText == res.result) {
        app.globalData.recoManager.stop();
      }
    }

    app.globalData.recoManager.onStop = function(res) {
      console.log("Has stopped");
      that.setData({
        'queText': res.result,
        'isSpeaking': false,
        'textareaWidth': res.result.length * 36,
      })
      console.log("queText is:" + that.data.queText);
      var msg = JSON.stringify({
        "type": "text",
        "method": "add",
        "data": that.data.queText,
      })
      wx.sendSocketMessage({
        "data": msg
      });
    }

    app.globalData.innerAudioContext.onPlay(() => {
      console.log('开始播放')
    })

    app.globalData.innerAudioContext.onError((res) => {
      console.log(res.errMsg)
      console.log(res.errCode)
    })


    console.log(app.globalData.recoManager);

    this.getCode();


    // this.sendHead();

    // 愚蠢的微信非要加上这个代码才能在ios上播放语音
    wx.setInnerAudioOption({
      "obeyMuteSwitch": false,
    })

    this.tryEncode();

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function() {

  },

  /**
   * 切换语音输入或文字输入
   */
  setInputVoice: function() {
    this.setData({
      voiceInput: !this.data.voiceInput
    })
  },

  /**
   * 从data文件夹中获取data
   */
  getData: function() {
    var feed_data = index.data;
    this.setData({
      queAndAns: feed_data,
      queAndAnsLength: feed_data.length
    })
    console.log(this.data.queAndAns);
    console.log(this.data.queAndAnsLength);
  },

  /**
   * 文本输入框输入
   */
  textInput: function(e) {
    /**
     * wxml里面的值是根据数据渲染界面的
     * 如果想要根据界面修改代码我们还是需要在这里添加函数
     */
    // this.data.queText = e.detail.value;
    this.data.textInput = e.detail.value;
  },

  /**
   * 发送文字消息
   */
  sendTextMessage: function() {
    var that = this;

    var temArr = that.data.queAndAns;
    console.log(that.data);

    if (!(this.isEmpty(this.data.ansText))) {
      console.log(that.data.ansText);
      temArr.push({
        "questionId": temArr.length,
        "question": that.data.queText,
        "answer": that.data.ansText
      });
      console.debug(temArr[temArr.length - 1].answer)
      that.setData({
        queAndAns: temArr,
        curTextArea: 'que-user',
        // textInput: '',
        queText: '',
        ansText: '',
      });
    }

    console.log("inputText is:" + that.data.inputText);
    var msg = JSON.stringify({
      "type": "text",
      "method": "add",
      "data": that.data.textInput,
    })
    wx.sendSocketMessage({
      "data": msg
    });

    console.log("The setData may not be done")
    this.setData({
      'textareaShow': true,
      'textShow': false,
      'queText': that.data.textInput,
      'textareaWidth': that.data.textInput.length * 36
    })

    console.log(this.data);

    // var temArr = that.data.queAndAns;
    // temArr[temArr.length - 1].question = that.data.queText;
    // console.log(temArr[temArr.length - 1].question)

    // this.query.select("#textInput");
  },

  /**
   * 滚动框滚动到最上方后聊天数组扩展
   */
  scrollToUpper: function() {
    var temArr = this.data.queAndAns;
    var indexArr = require('../../data/data_index.js').index.data;
    console.log(indexArr);
    // for (var i in indexArr) {
    //   temArr.unshift(i);
    // }
    indexArr = indexArr.concat(temArr);
    console.log(indexArr);
    this.setData({
      queAndAns: indexArr
    })
  },

  /**
   * 点击设置按钮的跳转
   */
  settingBindTap: function() {
    wx.navigateTo({
      // url: '../logs/logs'
      url: '../setting/setting'
    })
  },

  /**
   * 微信登录获取code
   */
  getCode: function() {
    var that = this;
    wx.login({
      success(res) {
        if (res.code) {
          console.log(res.code);
          that.setData({
            "code": res.code,
          })
        } else {
          console.log('登录失败！' + res.errMsg)
        }
      }
    })
  },

  /**
   * 使用微信同声传译获取进行语音合成
   */
  getVoice: function(text) {
    var that = this;
    app.globalData.recoPlugin.textToSpeech({
      lang: "zh_CN",
      tts: true,
      // content: "Finty（小芬）——AI个人助手与理财顾问，是一款集日常生活服务与个性化投资推荐于一体的AI智能对话机器人。使用者可以通过语音或文字输入的方式与它进行交互。生动的对话系统使它能对用户的话语做出准确回答，让用户获得像与好友交流般的愉快体验。经过一段时间的学习，它将越来越了解用户的行为习惯，从而为用户提供更加个性化的理财帮助，推荐最合适的理财产品，实现收益最大化。",
      content: text,
      success: function(res) {
        console.log(text);
        console.log("succ tts", res.filename)
        // var tempFile = that.doLoadVideo(res.filename);
        app.globalData.innerAudioContext.src = res.filename;
        app.globalData.innerAudioContext.play();
        console.log(app.globalData.innerAudioContext);
      },
      fail: function(res) {
        console.log("fail tts", res)
      }
    })
    console.log(app.globalData.innerAudioContext.src);

  },

  /**
   * 下载音频
   */
  doLoadVideo: function(src) {
    console.log("doLoadVideo begin");
    console.log(src);
    var tempFile;
    wx.downloadFile({
      url: src,
      success: function(res) {
        console.log("success:");
        console.log(res);
        tempFile = res.tempFilePath;
        console.log(tempFile);
        app.globalData.innerAudioContext.src = tempFile;
        console.log("The voice is from dowload video!");
        app.globalData.innerAudioContext.play();
        console.log(app.globalData.innerAudioContext);
      },
      fail: function() {
        console.log("aaa");
      }
    })
    return tempFile;
  },

  /**
   * textArea收到编辑
   */
  queTextReset: function(e) {
    var that = this;
    this.data.queText = e.detail.value;
    console.log(that.data.queText.length);
    that.setData({
      'textareaWidth': (that.data.queText.length * 36 > 540 ? 540 : that.data.queText.length * 36),
    })
  },

  /**
   * 新增ans的text并显示在界面上
   */
  addAnsAndShow: function(res) {
    // var temArr = this.data.queAndAns;
    // temArr[temArr.length - 1].answer = res;
    // console.log(temArr[temArr.length - 1].question)
    console.log(res);
    this.setData({
      'ansText': res,
      'textShow': true,
    })
    console.log("God tell me this:" + this.data.ansText);
    this.getVoice(res);
  },

  /**
   * 判断字符串是否为空
   */
  isEmpty: function(obj) {
    if (typeof obj == "undefined" || obj == null || obj == "") {
      return true;
    } else {
      return false;
    }
  },

  /**
   * 点击开始说话按钮
   */
  voiceInputBegin: function() {
    console.log("I won't give up!");

    var that = this;

    var temArr = that.data.queAndAns;

    if (!(this.isEmpty(this.data.ansText))) {
      console.log(that.data.ansText);
      temArr.push({
        "questionId": temArr.length,
        "question": that.data.queText,
        "answer": that.data.ansText
      });
      console.debug(temArr[temArr.length - 1].answer)
      that.setData({
        queAndAns: temArr,
        curTextArea: 'que-user',
        // textInput: '',
        queText: '',
        ansText: '',
      });
    }

    app.globalData.recoManager.start();
    this.setData({
      'textareaShow': true,
      'isSpeaking': true,
    })
  },

  /**
   * 点击停止说话按钮
   */
  voiceInputEnd: function() {
    app.globalData.recoManager.stop();
    console.log("How!")
    this.setData({
      'isSpeaking': false,
    })
  },

  /**
   * 用户完成对textArea的编辑后再次发送
   */
  queTextResend: function(e) {
    var that = this;
    this.data.queText = e.detail.value;
    var msg = JSON.stringify({
      "type": "text",
      "method": "reset",
      "data": that.data.queText,
    })
    wx.sendSocketMessage({
      "data": msg
    });
  },

  /**
   * 根据服务器返回的信息更改当前的answer的text
   */
  resetText: function(res) {
    this.setData({
      "ansText": res,
    })
    this.getVoice(res);
  },

  /**
   * 向后台发送头信息，包括code等信息
   */
  sendHead: function(res) {
    var that = this;
    var msg = JSON.stringify({
      "type": "head",
      "code": that.data.code
    })
    wx.sendSocketMessage({
      "data": msg
    });
  },

  /**
   * 向后台发送要求历史记录的请求
   */
  askHistory: function(number) {
    var msg = JSON.stringify({
      "type": "ask",
      "number": number
    })
    wx.sendSocketMessage({
      "data": msg
    });
  },

  /**
   * 向后台发送设置信息的请求
   */
  sendSetting: function(key, value) {
    var msg = JSON.stringify({
      "type": "setting",
      "key": key,
      "value": value,
    })
    wx.sendSocketMessage({
      "data": msg
    });
  },

  /**
   * 收到对发送的head信息的回复
   */
  getHead: function(res) {
    var obj = JSON.stringify(res);
    this.setData({
      "openId": obj.openId,
    })
  },

  /**
   * 收到历史记录
   */
  getHistory: function(res) {
    var that = this;
    var obj = JSON.stringify(res);
    var temArr = this.data.queAndAns;
    var indexArr = res.data
    console.log(indexArr);
    indexArr = indexArr.concat(temArr);
    console.log(indexArr);
    this.setData({
      "queAndAns": indexArr,
      "historyNum": that.data.historyNum + res.number,
    })
  },

  /**
   * 设置是否朗读文本
   */
  setSpeakAnswer: function(value) {
    this.setData({
      "speakAnswer": value
    })
  },

  /**
   * 删除历史记录
   */
  deleteHistory: function() {
    var that = this;
    var temArr = this.data.queAndAns.slice(
      that.data.historyNum,
      that.data.queAndAns.length
    );
  },

  tryEncode:function(){
    var s = "你好".encode('utf8');
    console.log("encode尝试:"+s);

  }


})