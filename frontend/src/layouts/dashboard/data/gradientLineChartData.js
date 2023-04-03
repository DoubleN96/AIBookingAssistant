/**
=========================================================
* Soft UI Dashboard React - v4.0.0
=========================================================

* Product Page: https://www.creative-tim.com/product/soft-ui-dashboard-react
* Copyright 2022 Creative Tim (https://www.creative-tim.com)

Coded by www.creative-tim.com

 =========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
*/

const gradientLineChartData = {
  labels: ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
  datasets: [
    {
      label: "Registerd via Chat",
      color: "success",
      data: [50, 40, 300, 220, 500, 250, 400, 230, 500],
    },
    {
      label: "Inquiries via Chat",
      color: "dark",
      data: [40, 90, 40, 140, 290, 290, 340, 230, 400],
    },
    {
      label: "Bookings via Chat",
      color: "warning",
      data: [30, 80, 330, 140, 290, 290, 340, 230, 400],
    },
  ],
};

export default gradientLineChartData;
