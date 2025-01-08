<script setup>
import ProductService from "@/service/ProductService";
import PhotoService from "@/service/PhotoService";
import { useLayout } from "@/layout/composables/layout";
import NodeService from "@/service/NodeService";
import { onMounted, ref, watch } from "vue";
import * as echarts from "echarts";
import {
  GridComponent,
  LegendComponent,
  MarkLineComponent,
  MarkPointComponent,
  TitleComponent,
  ToolboxComponent,
  TooltipComponent
} from "echarts/components";
import { LineChart } from "echarts/charts";
import { UniversalTransition } from "echarts/features";
import { CanvasRenderer } from "echarts/renderers";
import swal from "sweetalert";
import axios from "axios";

const { layoutConfig } = useLayout();
let documentStyle = getComputedStyle(document.documentElement);
let textColor = documentStyle.getPropertyValue("--text-color");
let textColorSecondary = documentStyle.getPropertyValue("--text-color-secondary");
let surfaceBorder = documentStyle.getPropertyValue("--surface-border");

const { isDarkTheme } = useLayout();
const products = ref([]);
const images = ref([]);
const lineOptions = ref(null);
const productService = new ProductService();
const photoService = new PhotoService();
const treeTableValue = ref(null);
const model1Value = ref(null);
const nodeService = new NodeService();
const lineData = ref(null);
const pieData = ref(null);
const polarData = ref(null);
const barData = ref(null);
const radarData = ref(null);

const pieOptions = ref(null);
const polarOptions = ref(null);
const barOptions = ref(null);
const radarOptions = ref(null);

const setColorOptions = () => {
  documentStyle = getComputedStyle(document.documentElement);
  textColor = documentStyle.getPropertyValue("--text-color");
  textColorSecondary = documentStyle.getPropertyValue("--text-color-secondary");
  surfaceBorder = documentStyle.getPropertyValue("--surface-border");
};
const setChart = () => {
  barData.value = {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [
      {
        label: "My First dataset",
        backgroundColor: documentStyle.getPropertyValue("--primary-500"),
        borderColor: documentStyle.getPropertyValue("--primary-500"),
        data: [65, 59, 80, 81, 56, 55, 40]
      },
      {
        label: "My Second dataset",
        backgroundColor: documentStyle.getPropertyValue("--primary-200"),
        borderColor: documentStyle.getPropertyValue("--primary-200"),
        data: [28, 48, 40, 19, 86, 27, 90]
      }
    ]
  };
  barOptions.value = {
    plugins: {
      legend: {
        labels: {
          fontColor: textColor
        }
      }
    },
    scales: {
      x: {
        ticks: {
          color: textColorSecondary,
          font: {
            weight: 500
          }
        },
        grid: {
          display: false,
          drawBorder: false
        }
      },
      y: {
        ticks: {
          color: textColorSecondary
        },
        grid: {
          color: surfaceBorder,
          drawBorder: false
        }
      }
    }
  };

  pieData.value = {
    labels: ["A", "B", "C"],
    datasets: [
      {
        data: [540, 325, 702],
        backgroundColor: [documentStyle.getPropertyValue("--indigo-500"), documentStyle.getPropertyValue("--purple-500"), documentStyle.getPropertyValue("--teal-500")],
        hoverBackgroundColor: [documentStyle.getPropertyValue("--indigo-400"), documentStyle.getPropertyValue("--purple-400"), documentStyle.getPropertyValue("--teal-400")]
      }
    ]
  };

  pieOptions.value = {
    plugins: {
      legend: {
        labels: {
          usePointStyle: true,
          color: textColor
        }
      }
    }
  };

  lineData.value = {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [
      {
        label: "First Dataset",
        data: [65, 59, 80, 81, 56, 55, 40],
        fill: false,
        backgroundColor: documentStyle.getPropertyValue("--primary-500"),
        borderColor: documentStyle.getPropertyValue("--primary-500"),
        tension: 0.4
      },
      {
        label: "Second Dataset",
        data: [28, 48, 40, 19, 86, 27, 90],
        fill: false,
        backgroundColor: documentStyle.getPropertyValue("--primary-200"),
        borderColor: documentStyle.getPropertyValue("--primary-200"),
        tension: 0.4
      }
    ]
  };

  lineOptions.value = {
    plugins: {
      legend: {
        labels: {
          fontColor: textColor
        }
      }
    },
    scales: {
      x: {
        ticks: {
          color: textColorSecondary
        },
        grid: {
          color: surfaceBorder,
          drawBorder: false
        }
      },
      y: {
        ticks: {
          color: textColorSecondary
        },
        grid: {
          color: surfaceBorder,
          drawBorder: false
        }
      }
    }
  };

  polarData.value = {
    datasets: [
      {
        data: [10, 16, 7, 3],
        backgroundColor: [documentStyle.getPropertyValue("--indigo-500"), documentStyle.getPropertyValue("--purple-500"), documentStyle.getPropertyValue("--teal-500"), documentStyle.getPropertyValue("--orange-500")],
        label: "My dataset"
      }
    ],
    labels: ["Indigo", "Purple", "Teal", "Orange"]
  };

  polarOptions.value = {
    plugins: {
      legend: {
        labels: {
          color: textColor
        }
      }
    },
    scales: {
      r: {
        grid: {
          color: surfaceBorder
        }
      }
    }
  };

  radarData.value = {
    labels: ["Eating", "Drinking", "Sleeping", "Designing", "Coding", "Cycling", "Running"],
    datasets: [
      {
        label: "My First dataset",
        borderColor: documentStyle.getPropertyValue("--indigo-400"),
        pointBackgroundColor: documentStyle.getPropertyValue("--indigo-400"),
        pointBorderColor: documentStyle.getPropertyValue("--indigo-400"),
        pointHoverBackgroundColor: textColor,
        pointHoverBorderColor: documentStyle.getPropertyValue("--indigo-400"),
        data: [65, 59, 90, 81, 56, 55, 40]
      },
      {
        label: "My Second dataset",
        borderColor: documentStyle.getPropertyValue("--purple-400"),
        pointBackgroundColor: documentStyle.getPropertyValue("--purple-400"),
        pointBorderColor: documentStyle.getPropertyValue("--purple-400"),
        pointHoverBackgroundColor: textColor,
        pointHoverBorderColor: documentStyle.getPropertyValue("--purple-400"),
        data: [28, 48, 40, 19, 96, 27, 100]
      }
    ]
  };

  radarOptions.value = {
    plugins: {
      legend: {
        labels: {
          fontColor: textColor
        }
      }
    },
    scales: {
      r: {
        grid: {
          color: textColorSecondary
        }
      }
    }
  };
};

const applyLightTheme = () => {
  lineOptions.value = {
    plugins: {
      legend: {
        labels: {
          color: "#495057"
        }
      }
    },
    scales: {
      x: {
        ticks: {
          color: "#495057"
        },
        grid: {
          color: "#ebedef"
        }
      },
      y: {
        ticks: {
          color: "#495057"
        },
        grid: {
          color: "#ebedef"
        }
      }
    }
  };
};
const applyDarkTheme = () => {
  lineOptions.value = {
    plugins: {
      legend: {
        labels: {
          color: "#ebedef"
        }
      }
    },
    scales: {
      x: {
        ticks: {
          color: "#ebedef"
        },
        grid: {
          color: "rgba(160, 167, 181, .3)"
        }
      },
      y: {
        ticks: {
          color: "#ebedef"
        },
        grid: {
          color: "rgba(160, 167, 181, .3)"
        }
      }
    }
  };
};

echarts.use([TitleComponent, ToolboxComponent, TooltipComponent, GridComponent, LegendComponent, MarkLineComponent, MarkPointComponent, LineChart, CanvasRenderer, UniversalTransition]);

onMounted(() => {
  productService.getProductsSmall().then((data) => (products.value = data));
  photoService.getImages().then((data) => (images.value = data));
  nodeService.getTreeTableNodes().then((data) => (treeTableValue.value = data));
  nodeService.getModel1Nodes().then((data) => (model1Value.value = data));
});

var read = function(name) {
  return JSON.parse(localStorage.getItem(name)); //把本地存储的my转成数组
};
// 在Vue3中，渲染完后执行函数
onMounted(() => {
  //调用需要执行的方法
  const ust = localStorage.getItem("ust");
  // console.log(ust);
  if (ust) {
    let usn = localStorage.getItem("usn");
    let st = localStorage.getItem("st");
    let et = localStorage.getItem("et");
    let ust = localStorage.getItem("ust");
    let uet = localStorage.getItem("uet");
    // console.log(usn);
    document.getElementById("Fan").innerHTML = "已选择的风机代号为：" + usn;
    document.getElementById("TimeRange").innerHTML = "对应的时间范围为：" + st + "~" + et;
    document.getElementById("UserTimeRange").innerHTML = "用户选择的时间范围为：" + ust + "~" + uet;
  }
});

watch(
  isDarkTheme,
  (val) => {
    if (val) {
      applyDarkTheme();
    } else {
      applyLightTheme();
    }
  },
  { immediate: true }
);

watch(
  layoutConfig.theme,
  () => {
    setColorOptions();
    setChart();
  },
  { immediate: true }
);


// const coopCachetImg = ref([]);
// 发送请求到后端进行预测
const VideoSample = () => {
  const fj = selectedfj.value;
  function show(cfg) {
    swal({
      closeOnClickOutside: false,
      closeOnEsc: false,
      // 解构cfg对象，展开cfg对象所有属性
      ...cfg
    });
  }
  if (fj) {
    const method = fj.name;
    // 将url图片转为base64
    var videoURL = document.getElementById("videosample").src;
    // 发送请求
    show({
      title: "提示",
      text: "正在进行视频推理，请稍等...",
      icon: "info",
      button: false
    });
    axios
      .post("http://39.104.62.62:5000/modelinfervideo", {
        method,
        videoURL
      })
      .then((res) => {
        const ret = res.data;
        console.log(ret);
        if (ret.code) {
          // 错误
          show({
            title: "错误",
            text: ret.data.msg,
            icon: "error",
            button: {
              text: "好的"
            }
          });
        } else {

          // 成功
          console.log(ret.data);
          const infer_video_url = "http://39.104.62.62:8877/" + ret.data.infer_video;
          // const infer_video = document.getElementById("videosample");
          // // console.log(infer_video_url);
          // // infer_video.src = infer_video_url;
          // onMounted(() => {
          //   document.getElementById("videosample").src = infer_video_url;
          // });

          // const a = document.createElement('a');
          // a.href = infer_video_url;
          // a.download = 'infer_video.mp4';
          // a.click();
          // window.open(infer_video_url);
          // window.download = infer_video_url;
          show({
            title: "成功",
            text: "视频推理成功,点击确定下载推理视频",
            icon: "success",
            button: {
              text: "确定"
            }
          });
          // axios下载文件
          axios({
            method: "get",
            url: infer_video_url,
            responseType: "blob"
          }).then((res) => {
            const link = document.createElement("a");
            const blob = new Blob([res.data]);
            link.style.display = "none";
            link.href = URL.createObjectURL(blob);
            link.download = "infer_video.mp4";
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
          });

          // axios

          //   .get(infer_json_url)
          //   .then((res) => {
          //     const jsonStr = JSON.stringify(res.data);
          //     console.log(jsonStr);
          //     document.getElementById("Fan").innerHTML = "返回结果：" + jsonStr;
          //   })
          //   .catch((err) => {
          //     console.log(err);
          //   });
          // document.getElementById('Fan').innerHTML = '返回结果：' + jsonStr;
        }
      })
      .catch((err) => {
        console.log(err);
      });
  } else {
    show({
      title: "错误",
      text: "请先选择推理模型",
      icon: "error",
      button: {
        text: "好的"
      }
    });
  }
};

// 提供给Dropdown组件使用的数据
const selectedfjs = ref([
  { name: "Picodet-xs", code: "1" },
  { name: "Picodet-s", code: "2" },
  { name: "PP-YOLO-Tiny", code: "3" },
  { name: "PP-YOLO-MobileNetV3-s", code: "4" },
  { name: "PP-YOLOE-crn-s", code: "5" },
  { name: "PP-YOLOE-crn-l", code: "6" },
  { name: "PP-YOLOE-plus-crn-s", code: "7" },
  { name: "PP-YOLOE-plus-crn-l", code: "8" },
  { name: "PP-YOLOv2", code: "9" },
  { name: "YOLOX-Tiny", code: "10" },
  { name: "YOLOX-cdn-Tiny", code: "11" }
]);
const selectedfj = ref(null);


// 根据风机代号发送请求到后端获取数据信息
const VideoInference = () => {
  const fj = selectedfj.value;
  function show(cfg) {
    swal({
      closeOnClickOutside: false,
      closeOnEsc: false,
      // 解构cfg对象，展开cfg对象所有属性
      ...cfg
    });
  }
  if (fj) {
    const method = fj.name;
    // 发送请求
    show({
      title: "提示",
      text: "正在进行视频推理，请稍等...",
      icon: "info",
      button: false
    });
    axios
      .post("http://39.104.62.62:5000/VideoInference", {
        method
      })
      .then((res) => {
        const ret = res.data;
        console.log(ret);
        if (ret.code) {
          // 错误
          show({
            title: "错误",
            text: ret.data.msg,
            icon: "error",
            button: {
              text: "好的"
            }
          });
        } else {

          // 成功
          console.log(ret.data);
          const infer_video_url = "http://39.104.62.62:8877/" + ret.data.infer_video;
          show({
            title: "成功",
            text: "视频推理成功,点击确定下载推理视频",
            icon: "success",
            button: {
              text: "确定"
            }
          });
          // axios下载文件
          axios({
            method: "get",
            url: infer_video_url,
            responseType: "blob"
          }).then((res) => {
            const link = document.createElement("a");
            const blob = new Blob([res.data]);
            link.style.display = "none";
            link.href = URL.createObjectURL(blob);
            link.download = "infer_video.mp4";
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
          });
        }
      })
      .catch((err) => {
        console.log(err);
      });
  } else {
    show({
      title: "错误",
      text: "请先选择推理模型",
      icon: "error",
      button: {
        text: "好的"
      }
    });
  }
};


import { useToast } from "primevue/usetoast";
const toast = useToast();

const onUpload = () => {
  toast.add({ severity: "info", summary: "Success", detail: "File Uploaded", life: 3000 });
//
};

</script>

<template>
  <!-- 列表 -->
  <div class="">
    <div class="card">
      <h5>部分模型介绍，更多模型及性能细节对比请点击左侧Github/Gitee链接进行查看</h5>
      <TreeTable :value="model1Value"  v-model:selectionKeys="selectedTreeTableValue">
        <Column field="model" header="模型"></Column>
        <Column field="parameter" header="参数量（MB）"></Column>
        <Column field="mAP" header="mAP0.5"></Column>
        <Column field="Introduction" header="介绍"></Column>
      </TreeTable>
    </div>
  </div>
  <!--   添加div选择模型的选项-->
  <div class="fj-grid" id="Fj">
    <div class="card" id="FjSelect">
      <h5>模型选择</h5>
      <!--      使用main.js中的Dropdown来选择推理-->
      <!--令选择框和按钮居中-->
      <div class="p-d-flex p-jc-center">
        <Dropdown v-model="selectedfj" :options="selectedfjs" optionLabel="name"
                  placeholder="请选择一个推理模型"></Dropdown>
        <!--          令Dropdown与Button在同一行间存在少许间隙-->
        <br />
        <br />
        <!--        <Button label="确定" @click="onSelect"></Button>-->
      </div>
    </div>
  </div>


  <div class="card">
    <h5>Video Sample</h5>
    <Carousel :value="products" :numVisible="1" :numScroll="1" :circular="false"
              :responsiveOptions="carouselResponsiveOptions">
      <template #item="product">
        <div class="product-item">
          <div class="product-item-content">
            <div class="mb-3">
<!--              <Image :src="'http://39.104.62.62:8877/images/' + product.data.image" :alt="product.data.name" id="imgsample" class="product-image" />-->
              <video :src="'http://39.104.62.62:8877/static/video/test1.mp4'" id="videosample" class="product-image" autoplay controls preload="auto" />
            </div>
            <div>
              <div class="car-buttons mt-5">
                <Button type="button" class="p-button p-button-rounded mr-2" icon="pi pi-search" @click="VideoSample()"></Button>
                <!--<Button type="button" class="p-button-success p-button-rounded mr-2" icon="pi pi-star-fill"></Button>-->
                <!--<Button type="button" class="p-button-help p-button-rounded" icon="pi pi-cog"></Button>-->
              </div>
            </div>
          </div>
        </div>
      </template>
    </Carousel>
  </div>


  <div class="grid p-fluid">
    <div class="col-12 md:col-12">
      <Button label="视频推理" class="mr-2 mb-2" @click="VideoInference" />
    </div>
  </div>

  <div class="grid">
    <div class="col-12 md:col-12">
      <div class="card">
        <Toast />
        <h5>上传视频</h5>
        <FileUpload name="demo[]"
                    url="http://39.104.62.62:5000/UploadVideo"
                    @uploader="onUpload()"
                    accept="video/*"
                    :multiple="false"
                    :maxFileSize="10000000000"
                    id="uploadfile">
          <template #empty>
            <p>Drag and drop files to here to upload.</p>
          </template>
        </FileUpload>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '@/assets/demo/styles/badges.scss';
@import '@/assets/demo/styles/items.scss';
</style>
