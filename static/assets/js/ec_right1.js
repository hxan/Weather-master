var ec_right1 = echarts.init(document.getElementById('r1'),"dark");

var option_right1 = {

	backgroundColor: '#00008B',

	title: {
		text: '气压(Pa)',
		// subtext: '模拟数据',
		// x: 'center',
	  textStyle: {
		  
	  },
	  right: 'left'
	},

	//  图表距边框的距离,可选值：'百分比'¦ {number}（单位px）
	grid: {
		top: 50, // 等价于 y: '16%'
		right: '4%',
		right: '6%',
		bottom: '4%',
		containLabel: true
	},

	// 提示框
	tooltip: {
		trigger: 'axis',
	  axisPointer: {
		  type: 'line',
		  lineStyle: {
			  color: '#7171C6'
		  }
	  }
	},

	//工具框，可以选择
	toolbox: {
		feature: {
			saveAsImage: {} //下载工具
		}
	},

	xAxis: {
		// name: '周几',
		type: 'category',
		// axisLine: {
		// 	lineStyle: {
		// 		// 设置x轴颜色
		// 		color: '#912CEE'
		// 	}
		// },
		// // 设置X轴数据旋转倾斜
		// axisLabel: {
		// 	rotate: 30, // 旋转角度
		// 	interval: 0 //设置X轴数据间隔几个显示一个，为0表示都显示
		// },
		// // boundaryGap值为false的时候，折线第一个点在y轴上
		// boundaryGap: false,
		data: ['1小时','2小时','3小时','4小时','5小时']
	},

	yAxis: {
		// name: '数值',
		type: 'value',
		min: 800, // 设置y轴刻度的最小值
		max: 1800, // 设置y轴刻度的最大值
		splitNumber: 10, // 设置y轴刻度间隔个数
		axisLine: {
		  show: true
			// lineStyle: {
			// 	// 设置y轴颜色
			// 	color: '#87CEFA'
			// }
		},
	  axisLabel: {
		  show: true,
		  color: 'white',
		  fontSize: 12,
		  formatter: function(value) {
			  if (value >= 1000) {
				  value = value / 1000 + 'k';
			  }
			  return value;
		  }
	  },
	  splitLine: {
		  show: true,
		  lineStyle: {
			  color: '#172738',
			  width: 1,
			  type: 'solid'
		  }
	  }
	},

	series: [{
			name: 'wind speed',
			data: [1500,1641,1239,1103,990],
			type: 'line',
			// 设置小圆点消失
			// 注意：设置symbol: 'none'以后，拐点不存在了，设置拐点上显示数值无效
			// symbol: 'none',
			// 设置折线弧度，取值：0-1之间
			smooth: true
		}
	]

	// color: ['#00EE00', '#FF9F7F', '#FFD700']
};

ec_right1.setOption(option_right1);
