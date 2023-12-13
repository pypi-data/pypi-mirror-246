"""
  MechViz -- Python-based toolkit for the analysis and visualization of mechanical properties of materials

  Copyright (C) 2019-2024 by Chinedu Ekuma

  This program is free software; you can redistribute it and/or modify it under the
  terms of the GNU General Public License as published by the Free Software Foundation
  version 3 of the License.

  This program is distributed in the hope that it will be useful, but WITHOUT ANY
  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
  PARTICULAR PURPOSE.  See the GNU General Public License for more details.

  E-mail: cekuma1@gmail.com

"""

def calc_elastic_constants_standalone(symmetry,dimensional, elastic_tensor,elastic_constants_dict):

    if dimensional == "3D":
        c11 = elastic_tensor[0, 0]
        c12 = elastic_tensor[0, 1]
        c13 = elastic_tensor[0, 2]
        c14 = elastic_tensor[0, 3]
        c15 = elastic_tensor[0, 4]
        c16 = elastic_tensor[0, 5]

        c21 = elastic_tensor[1, 0]
        c22 = elastic_tensor[1, 1]
        c23 = elastic_tensor[1, 2]
        c24 = elastic_tensor[1, 3]
        c25 = elastic_tensor[1, 4]
        c26 = elastic_tensor[1, 5]

        c31 = elastic_tensor[2, 0]
        c32 = elastic_tensor[2, 1]
        c33 = elastic_tensor[2, 2]
        c34 = elastic_tensor[2, 3]
        c35 = elastic_tensor[2, 4]
        c36 = elastic_tensor[2, 5]

        c41 = elastic_tensor[3, 0]
        c42 = elastic_tensor[3, 1]
        c43 = elastic_tensor[3, 2]
        c44 = elastic_tensor[3, 3]
        c45 = elastic_tensor[3, 4]
        c46 = elastic_tensor[3, 5]

        c51 = elastic_tensor[4, 0]
        c52 = elastic_tensor[4, 1]
        c53 = elastic_tensor[4, 2]
        c54 = elastic_tensor[4, 3]
        c55 = elastic_tensor[4, 4]
        c56 = elastic_tensor[4, 5]

        c61 = elastic_tensor[5, 0]
        c62 = elastic_tensor[5, 1]
        c63 = elastic_tensor[5, 2]
        c64 = elastic_tensor[5, 3]
        c65 = elastic_tensor[5, 4]
        c66 = elastic_tensor[5, 5]
        try:
          if symmetry == "Cubic":

              B_v = (c11+2*c12)/3.
              B_r = B_v

              G_v = (c11-c12+3*c44)/5.
              G_r = 5*(c11-c12)*c44/(4*c44+3*(c11-c12))

              B_vrh = (B_v+B_r)/2.
              G_vrh = (G_v+G_r)/2.
              E = 9*B_vrh*G_vrh/(3*B_vrh+G_vrh)
              v = (3*B_vrh-2*G_vrh)/(2*(3*B_vrh+G_vrh))

              elastic_constants_dict['c11'] = c11
              elastic_constants_dict['c12'] = c12
              elastic_constants_dict['c44'] = c44

              elastic_constants_dict['B_v'] = B_v
              elastic_constants_dict['B_r'] = B_r
              elastic_constants_dict['G_v'] = G_v
              elastic_constants_dict['G_r'] = G_r
              elastic_constants_dict['B_vrh'] = B_vrh
              elastic_constants_dict['G_vrh'] = G_vrh
              elastic_constants_dict['E'] = E
              elastic_constants_dict['v'] = v
          elif symmetry == "Hexagonal":

              M = c11+c12+2*c33-4*c13
              C2 = (c11+c12)*c33-2*c13*c13
              c66 = (c11-c12)/2.

              B_v = (2*(c11+c12)+4*c13+c33)/9.
              G_v = (M+12*c44+12*c66)/30.
              B_r = C2/M
              G_r = 2.5*(C2*c44*c66)/(3*B_v*c44*c66+C2*(c44+c66))

              B_vrh = (B_v+B_r)/2.
              G_vrh = (G_v+G_r)/2.
              E = 9*B_vrh*G_vrh/(3*B_vrh+G_vrh)
              v = (3*B_vrh-2*G_vrh)/(2*(3*B_vrh+G_vrh))

              elastic_constants_dict['c11'] = c11
              elastic_constants_dict['c12'] = c12
              elastic_constants_dict['c13'] = c13
              elastic_constants_dict['c33'] = c33
              elastic_constants_dict['c44'] = c44

              elastic_constants_dict['B_v'] = B_v
              elastic_constants_dict['B_r'] = B_r
              elastic_constants_dict['G_v'] = G_v
              elastic_constants_dict['G_r'] = G_r
              elastic_constants_dict['B_vrh'] = B_vrh
              elastic_constants_dict['G_vrh'] = G_vrh
              elastic_constants_dict['E'] = E
              elastic_constants_dict['v'] = v  
          elif symmetry == "Trigonal1": 

              elastic_constants_dict['c11'] = c11
              elastic_constants_dict['c12'] = c12
              elastic_constants_dict['c13'] = c13
              elastic_constants_dict['c14'] = c14
              elastic_constants_dict['c33'] = c33
              elastic_constants_dict['c44'] = c44  

          elif symmetry == "Trigonal2":

              elastic_constants_dict['c11'] = c11
              elastic_constants_dict['c12'] = c12
              elastic_constants_dict['c13'] = c13
              elastic_constants_dict['c14'] = c14
              elastic_constants_dict['c15'] = c15
              elastic_constants_dict['c33'] = c33
              elastic_constants_dict['c44'] = c44 
          elif symmetry == "Tetragonal1":

              M = c11+c12+2*c33-4*c13
              C2 = (c11+c12)*c33-2*c13*c13

              B_v = (2*(c11+c12)+c33+4*c13)/9.
              G_v = (M+3*c11-3*c12+12*c44+6*c66)/30.
              B_r = C2/M
              G_r = 15./(18*B_v/C2+6/(c11-c12)+6/c44+3/c66)

              B_vrh = (B_v+B_r)/2.
              G_vrh = (G_v+G_r)/2.
              E = 9*B_vrh*G_vrh/(3*B_vrh+G_vrh)
              v = (3*B_vrh-2*G_vrh)/(2*(3*B_vrh+G_vrh))

              elastic_constants_dict['c11'] = c11
              elastic_constants_dict['c12'] = c12
              elastic_constants_dict['c13'] = c13
              elastic_constants_dict['c33'] = c33
              elastic_constants_dict['c44'] = c44
              elastic_constants_dict['c66'] = c66

              elastic_constants_dict['B_v'] = B_v
              elastic_constants_dict['B_r'] = B_r
              elastic_constants_dict['G_v'] = G_v
              elastic_constants_dict['G_r'] = G_r

              elastic_constants_dict['B_vrh'] = B_vrh
              elastic_constants_dict['G_vrh'] = G_vrh
              elastic_constants_dict['E'] = E
              elastic_constants_dict['v'] = v
          elif symmetry == "Tetragonal2":

              M = c11+c12+2*c33-4*c13
              C2 = (c11+c12)*c33-2*c13*c13

              B_v = (2*(c11+c12)+c33+4*c13)/9.
              G_v = (M+3*c11-3*c12+12*c44+6*c66)/30.
              B_r = C2/M
              G_r = 15./(18*B_v/C2+6/(c11-c12)+6/c44+3/c66)

              B_vrh = (B_v+B_r)/2.
              G_vrh = (G_v+G_r)/2.
              E = 9*B_vrh*G_vrh/(3*B_vrh+G_vrh)
              v = (3*B_vrh-2*G_vrh)/(2*(3*B_vrh+G_vrh))

              elastic_constants_dict['c11'] = c11
              elastic_constants_dict['c12'] = c12
              elastic_constants_dict['c13'] = c13
              elastic_constants_dict['c16'] = c16
              elastic_constants_dict['c33'] = c33
              elastic_constants_dict['c44'] = c44
              elastic_constants_dict['c66'] = c66

              elastic_constants_dict['B_v'] = B_v
              elastic_constants_dict['B_r'] = B_r
              elastic_constants_dict['G_v'] = G_v
              elastic_constants_dict['G_r'] = G_r

              elastic_constants_dict['B_vrh'] = B_vrh
              elastic_constants_dict['G_vrh'] = G_vrh
              elastic_constants_dict['E'] = E
              elastic_constants_dict['v'] = v
          elif symmetry == "Orthorombic":

              D = c13*(c12*c23-c13*c22)+c23*(c12*c13-c23*c11)+c33*(c11*c22-c12*c12)
              B_v = (c11+c22+c33+2*(c12+c13+c23))/9.
              G_v = (c11+c22+c33+3*(c44+c55+c66)-(c12+c13+c23))/15.
              B_r = D/(c11*(c22+c33-2*c23)+c22*(c33-2*c13)-2*c33*c12+c12*(2*c23-c12)+c13*(2*c12-c13)+c23*(2*c13-c23))
              G_r = 15/(4*(c11*(c22+c33+c23)+c22*(c33+c13)+c33*c12-c12*(c23+c12)-c13*(c12+c13)-c23*(c13+c23))/D+3*(1/c44+1/c55+1/c66))

              B_vrh = (B_v+B_r)/2.
              G_vrh = (G_v+G_r)/2.
              E = 9*B_vrh*G_vrh/(3*B_vrh+G_vrh)
              v = (3*B_vrh-2*G_vrh)/(2*(3*B_vrh+G_vrh))

              elastic_constants_dict['c11'] = c11
              elastic_constants_dict['c12'] = c12
              elastic_constants_dict['c13'] = c13
              elastic_constants_dict['c22'] = c22
              elastic_constants_dict['c23'] = c23
              elastic_constants_dict['c33'] = c33
              elastic_constants_dict['c44'] = c44
              elastic_constants_dict['c55'] = c55
              elastic_constants_dict['c66'] = c66

              elastic_constants_dict['B_v'] = B_v
              elastic_constants_dict['B_r'] = B_r
              elastic_constants_dict['G_v'] = G_v
              elastic_constants_dict['G_r'] = G_r
              elastic_constants_dict['B_vrh'] = B_vrh
              elastic_constants_dict['G_vrh'] = G_vrh
              elastic_constants_dict['E'] = E
              elastic_constants_dict['v'] = v
          elif symmetry == "Monoclinic":

              a = c33*c55-c35*c35
              b = c23*c55-c25*c35
              c = c13*c35-c15*c33
              d = c13*c55-c15*c35
              e = c13*c25-c15*c23
              f = c11*(c22*c55-c25*c25)-c12*(c12*c55-c15*c25)+c15*(c12*c25-c15*c22)+c25*(c23*c35-c25*c33)
              g = c11*c22*c33-c11*c23*c23-c22*c13*c13-c33*c12*c12+2*c12*c13*c23
              O = 2*(c15*c25*(c33*c12-c13*c23)+c15*c35*(c22*c13-c12*c23)+c25*c35*(c11*c23-c12*c13))-(c15*c15*(c22*c33-c23*c23)+c25*c25*(c11*c33-c13*c13)+c35*c35*(c11*c22-c12*c12))+g*c55

              B_v = (c11+c22+c33+2*(c12+c13+c23))/9.
              G_v = (c11+c22+c33+3*(c44+c55+c66)-(c12+c13+c23))/15.
              B_r = O/(a*(c11+c22-2*c12)+b*(2*c12-2*c11-c23)+c*(c15-2*c25)+d*(2*c12+2*c23-c13-2*c22)+2*e*(c25-c15)+f)
              G_r = 15/(4*(a*(c11+c22+c12)+b*(c11-c12-c23)+c*(c15+c25)+d*(c22-c12-c23-c13)+e*(c15-c25)+f)/O+3*(g/O+(c44+c66)/(c44*c66-c46*c46)))

              B_vrh = (B_v+B_r)/2.
              G_vrh = (G_v+G_r)/2.
              E = 9*B_vrh*G_vrh/(3*B_vrh+G_vrh)
              v = (3*B_vrh-2*G_vrh)/(2*(3*B_vrh+G_vrh))

              elastic_constants_dict['c11'] = c11
              elastic_constants_dict['c12'] = c12
              elastic_constants_dict['c13'] = c13
              elastic_constants_dict['c15'] = c15
              elastic_constants_dict['c22'] = c22
              elastic_constants_dict['c23'] = c23
              elastic_constants_dict['c25'] = c25
              elastic_constants_dict['c33'] = c33
              elastic_constants_dict['c35'] = c35
              elastic_constants_dict['c44'] = c44
              elastic_constants_dict['c46'] = c46
              elastic_constants_dict['c55'] = c55
              elastic_constants_dict['c66'] = c66

              elastic_constants_dict['B_v'] = B_v
              elastic_constants_dict['B_r'] = B_r
              elastic_constants_dict['G_v'] = G_v
              elastic_constants_dict['G_r'] = G_r
              elastic_constants_dict['B_vrh'] = B_vrh
              elastic_constants_dict['G_vrh'] = G_vrh
              elastic_constants_dict['E'] = E
              elastic_constants_dict['v'] = v
          elif symmetry == "Triclinic":

              elastic_constants_dict['c11'] = c11
              elastic_constants_dict['c12'] = c12
              elastic_constants_dict['c13'] = c13
              elastic_constants_dict['c14'] = c14
              elastic_constants_dict['c15'] = c15
              elastic_constants_dict['c16'] = c16
              elastic_constants_dict['c22'] = c22
              elastic_constants_dict['c23'] = c23
              elastic_constants_dict['c24'] = c24
              elastic_constants_dict['c25'] = c25
              elastic_constants_dict['c26'] = c26
              elastic_constants_dict['c33'] = c33
              elastic_constants_dict['c34'] = c34
              elastic_constants_dict['c35'] = c35
              elastic_constants_dict['c36'] = c36
              elastic_constants_dict['c44'] = c44
              elastic_constants_dict['c45'] = c45
              elastic_constants_dict['c46'] = c46
              elastic_constants_dict['c55'] = c55
              elastic_constants_dict['c56'] = c56
              elastic_constants_dict['c66'] = c66
          else:
              print("Crystal symmtry not determined. Check your structure")
        except Exception as e:
            print(f"Error reading crystal structure: {e}")
    elif dimensional == "2D":
          C11, C12, C16, _, C22, C26, _, _, C66 = elastic_tensor.ravel()
          elastic_constants_dict['c11'] = C11
          elastic_constants_dict['c22'] = C22
          elastic_constants_dict['c12'] = C12
          elastic_constants_dict['c16'] = C16
          elastic_constants_dict['c66'] = C66
    elif dimensional == "1D":
          c33 = elastic_tensor[2, 2]
          c23 = elastic_tensor[1, 2]
          c32 = elastic_tensor[2, 1]
          elastic_constants_dict['c33'] = c33
          elastic_constants_dict['c23'] = c23
          elastic_constants_dict['c32'] = c23
    return elastic_constants_dict



