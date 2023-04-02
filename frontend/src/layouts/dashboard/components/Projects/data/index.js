

// @mui material components
import Tooltip from "@mui/material/Tooltip";

// Soft UI Dashboard React components
import SoftBox from "components/SoftBox";
import SoftTypography from "components/SoftTypography";
import SoftAvatar from "components/SoftAvatar";
import SoftProgress from "components/SoftProgress";

// Images

import team1 from "assets/images/team-1.jpg";
import team2 from "assets/images/team-2.jpg";
import team3 from "assets/images/team-3.jpg";
import team4 from "assets/images/team-4.jpg";

export default function data() {
 

  return {
    columns: [
      { name: "tenants", align: "left" },
      { name: "unit", align: "center" },
      { name: "email", align: "center" },
    ],

    rows: [
      {
        tenants: [team1, "Zara Patel"],
        unit: (
          <SoftBox>
          <SoftTypography variant="h8" gutterBottom>
            Main flat
          </SoftTypography>
          <SoftBox display="flex" alignItems="center" lineHeight={0}>
          
            <SoftTypography variant="caption" fontWeight="regular" color="text">
              <strong>82 m2</strong>
            </SoftTypography>
          </SoftBox>
        </SoftBox>
        ),
        email: (
          <SoftTypography variant="caption" color="text" fontWeight="medium">
            zarap@yahoo.de
          </SoftTypography>
        ),
      },
      {
        tenants: [team2, "Theo Nguyen"],
        unit: (
          <SoftBox>
          <SoftTypography variant="h8" gutterBottom>
            Main flat
          </SoftTypography>
          <SoftBox display="flex" alignItems="center" lineHeight={0}>
          
            <SoftTypography variant="caption" fontWeight="regular" color="text">
              <strong>82 m2</strong>
            </SoftTypography>
          </SoftBox>
        </SoftBox>
        ),
        email: (
          <SoftTypography variant="caption" color="text" fontWeight="medium">
            theon@yahoo.com
          </SoftTypography>
        ),
      },
      {
        tenants: [team3, "Neil Khan"],
        unit: (
          <SoftBox>
          <SoftTypography variant="h8" gutterBottom>
            Main flat
          </SoftTypography>
          <SoftBox display="flex" alignItems="center" lineHeight={0}>
          
            <SoftTypography variant="caption" fontWeight="regular" color="text">
              <strong>82 m2</strong>
            </SoftTypography>
          </SoftBox>
        </SoftBox>
        ),

        email: (
          <SoftTypography variant="caption" color="text" fontWeight="medium">
           neilk@hotmail.com
          </SoftTypography>
        ),
      },
      {
        tenants: [team4, "Leo Fischer"],
        unit: (
          <SoftBox>
          <SoftTypography variant="h8" gutterBottom>
            Main flat
          </SoftTypography>
          <SoftBox display="flex" alignItems="center" lineHeight={0}>
          
            <SoftTypography variant="caption" fontWeight="regular" color="text">
              <strong>82 m2</strong>
            </SoftTypography>
          </SoftBox>
        </SoftBox>
        ),
        phone: (
          <SoftTypography variant="caption" color="text" fontWeight="medium">
             +48 588 789 124 111
          </SoftTypography>
        ),
        email: (
          <SoftTypography variant="caption" color="text" fontWeight="medium">
            leof@gmail.com
          </SoftTypography>
        ),
      
      },
    ],
  };
}

