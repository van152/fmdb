__int64 __fastcall sub_141189C60(__int64 a1, int a2, __int64 **a3)
{
  __int64 **v3; // rdi
  __int16 v5; // ax
  unsigned __int8 v6; // al
  __int16 v7; // cx
  __int16 v8; // ax
  char v9; // cl
  __int64 v10; // rax
  __int64 v11; // rax
  unsigned __int8 v12; // al
  __int64 v13; // rax
  unsigned __int8 v14; // al
  __int64 v15; // rax
  __int64 v16; // rdx
  __int64 v17; // rax
  __int64 v18; // rax
  __int64 v19; // rax
  int v20; // eax
  char v21; // al
  char v22; // cl
  __m128 v23; // xmm0
  __m128 v24; // xmm0
  __m128 v25; // xmm1
  __m128 v26; // xmm2
  int v27; // eax
  char v28; // al
  char v29; // cl
  __int64 v30; // rax
  __int64 v31; // rdx
  __int64 v32; // rcx
  __int64 v33; // rdx
  unsigned int *v34; // rdx
  unsigned int v35; // eax
  int v36; // ecx
  __m128 v37; // xmm0
  __m128 v38; // xmm0
  __m128 v39; // xmm1
  __m128 v40; // xmm2
  int v41; // eax
  __m128 v43; // xmm2
  __m128 v44; // xmm2
  __int64 v45; // [rsp+20h] [rbp-48h] BYREF
  _QWORD v46[3]; // [rsp+28h] [rbp-40h] BYREF
  __int64 *v47; // [rsp+40h] [rbp-28h] BYREF
  __int64 *v48; // [rsp+48h] [rbp-20h]

  v3 = a3;
  if ( a2 <= 1399743862 )
  {
    if ( a2 > 1399153528 )
    {
      if ( a2 > 1399615341 )
      {
        if ( a2 <= 1399683179 )
        {
          switch ( a2 )
          {
            case 1399615342:
              *(float *)(a1 + 100) = (*(float (__fastcall **)(__int64 *, __int64 **))(**a3 + 96))(*a3, a3);
              goto LABEL_171;
            case 1399680620:
              if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) != 0 )
                *(_WORD *)(a1 + 144) = (int)(float)(fminf(
                                                      fmaxf(
                                                        (*(float (__fastcall **)(__int64 *, __int64 **))(**v3 + 96))(
                                                          *v3,
                                                          v3),
                                                        MEMORY[0x14179E5F0]),
                                                      MEMORY[0x1417B609C])
                                                  * MEMORY[0x141775530]);
              else
                *(_WORD *)(a1 + 144) = 900;
              goto LABEL_171;
            case 1399680631:
              if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) != 0 )
                *(_WORD *)(a1 + 146) = (int)(float)(fminf(
                                                      fmaxf(
                                                        (*(float (__fastcall **)(__int64 *, __int64 **))(**v3 + 96))(
                                                          *v3,
                                                          v3),
                                                        MEMORY[0x14187DC74]),
                                                      MEMORY[0x14179E5F0])
                                                  * MEMORY[0x141775530]);
              else
                *(_WORD *)(a1 + 146) = 550;
              goto LABEL_171;
            default:
              break;
          }
        }
        else if ( a2 > 1399742828 )
        {
          if ( a2 == 1399742829 )
          {
            (*(void (__fastcall **)(__int64 *, __int64 *, __int64 **))(**a3 + 128))(*a3, &v45, a3);
            sub_140809100(a1 + 56, &v45);
            v32 = v45;
            if ( v45 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v45 - 4)) == 0 )
              sub_1412EC9A0(v32 - 4, v31);
            LODWORD(v3) = a1 + 72;
            LOWORD(v31) = 18;
            sub_140E45100(a1 + 72, v31);
            LOWORD(v33) = 30;
            sub_140E45100(a1 + 72, v33);
            LOBYTE(v3) = 1;
            if ( qword_141B602E8 == qword_141B602F0 )
              return (unsigned int)v3;
            v34 = (unsigned int *)(qword_141B602E8 + 56);
            if ( (unsigned __int64)(qword_141B602F0 - qword_141B602E8) < 0x39 )
              v34 = (unsigned int *)qword_141B602E8;
            v35 = *v34;
            if ( *v34 <= 0x18 )
            {
              v36 = 17335296;
              if ( _bittest(&v36, v35) )
              {
                *(_BYTE *)(a1 + 168) = 0;
                return (unsigned int)v3;
              }
              if ( v35 == 12 )
              {
                *(_BYTE *)(a1 + 168) = 3;
                return (unsigned int)v3;
              }
            }
            if ( v35 == 1000001 )
              *(_BYTE *)(a1 + 168) = 4;
            return (unsigned int)v3;
          }
          if ( a2 == 1399743091 )
          {
            sub_140FE7EA0(a1 + 88, a3);
            goto LABEL_171;
          }
        }
        else
        {
          if ( a2 == 1399683180 )
          {
            if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) != 0 )
              *(_WORD *)(a1 + 148) = (int)(float)(fminf(
                                                    fmaxf(
                                                      (*(float (__fastcall **)(__int64 *, __int64 **))(**v3 + 96))(
                                                        *v3,
                                                        v3),
                                                      MEMORY[0x14179E5F0]),
                                                    MEMORY[0x1417B609C])
                                                * MEMORY[0x141775530]);
            else
              *(_WORD *)(a1 + 148) = 900;
            goto LABEL_171;
          }
          if ( a2 == 1399683191 )
          {
            if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) != 0 )
              *(_WORD *)(a1 + 150) = (int)(float)(fminf(
                                                    fmaxf(
                                                      (*(float (__fastcall **)(__int64 *, __int64 **))(**v3 + 96))(
                                                        *v3,
                                                        v3),
                                                      MEMORY[0x14187DC74]),
                                                    MEMORY[0x14179E5F0])
                                                * MEMORY[0x141775530]);
            else
              *(_WORD *)(a1 + 150) = 550;
            goto LABEL_171;
          }
        }
        return sub_140FE2700((_DWORD *)a1, a2, a3);
      }
      if ( a2 > 1399420006 )
      {
        if ( a2 == 1399420007 )
        {
          *(_BYTE *)(a1 + 155) = *(_BYTE *)(a1 + 155) & 0xFB
                               | (4 * (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 48))(*a3, a3));
          goto LABEL_171;
        }
        if ( a2 != 1399605581 )
        {
          if ( a2 != 1399611764 )
            return sub_140FE2700((_DWORD *)a1, a2, a3);
          *(float *)(a1 + 96) = (*(float (__fastcall **)(__int64 *, __int64 **))(**a3 + 96))(*a3, a3);
          goto LABEL_171;
        }
        if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) == 0 )
        {
          *(_WORD *)(a1 + 140) = -1;
          goto LABEL_171;
        }
        if ( (*(int (__fastcall **)(__int64 *, __int64 **))(**v3 + 64))(*v3, v3) <= 0 )
        {
          v23.m128_f32[0] = (float)*(__int16 *)(a1 + 136) / MEMORY[0x141775530];
          v43 = _mm_cmpge_ss((__m128)MEMORY[0x141759000], v23);
          v23.m128_f32[0] = fminf(fmaxf(v23.m128_f32[0], MEMORY[0x14179E5F0]), MEMORY[0x1417B609C])
                          * MEMORY[0x141775530];
          v27 = (int)COERCE_FLOAT(MEMORY[0x1417E35FC] & v43.m128_i32[0] | _mm_andnot_ps(v43, v23).m128_u32[0]);
          goto LABEL_168;
        }
LABEL_134:
        *(double *)v24.m128_u64 = (*(double (__fastcall **)(__int64 *, __int64 **))(**v3 + 96))(*v3, v3);
        v25 = v24;
        v26 = _mm_cmpge_ss((__m128)MEMORY[0x141759000], v24);
        v25.m128_f32[0] = fminf(fmaxf(v24.m128_f32[0], MEMORY[0x14179E5F0]), MEMORY[0x1417B609C]) * MEMORY[0x141775530];
        v27 = (int)COERCE_FLOAT(MEMORY[0x1417E35FC] & v26.m128_i32[0] | _mm_andnot_ps(v26, v25).m128_u32[0]);
LABEL_168:
        *(_WORD *)(a1 + 140) = v27;
        goto LABEL_171;
      }
      if ( a2 == 1399153529 )
      {
        *(_DWORD *)(a1 + 124) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
        goto LABEL_171;
      }
      if ( a2 == 1399156342 )
      {
        *(_BYTE *)(a1 + 160) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
        goto LABEL_171;
      }
      if ( a2 != 1399158900 )
        return sub_140FE2700((_DWORD *)a1, a2, a3);
      v9 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 48))(*a3, a3) | *(_BYTE *)(a1 + 155) & 0xFE;
LABEL_158:
      *(_BYTE *)(a1 + 155) = v9;
      goto LABEL_171;
    }
    if ( a2 <= 1399025762 )
    {
      if ( a2 > 1398959203 )
      {
        if ( a2 == 1398959204 )
        {
          v19 = sub_140DBC940();
          sub_140DBCA60(v19, &v45, v3);
          *(_DWORD *)(a1 + 40) = v45;
          goto LABEL_171;
        }
        if ( a2 == 1399021939 )
        {
          if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) != 0 )
          {
            v20 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**v3 + 64))(*v3, v3);
            *(_DWORD *)(a1 + 120) = v20;
            LOBYTE(v3) = 1;
            if ( v20 <= 0 )
              *(_DWORD *)(a1 + 120) = *(_DWORD *)(a1 + 108);
            return (unsigned int)v3;
          }
          *(_DWORD *)(a1 + 120) = 0;
          goto LABEL_171;
        }
        if ( a2 != 1399025526 )
          return sub_140FE2700((_DWORD *)a1, a2, a3);
        LOBYTE(v8) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 48))(*a3, a3);
        v7 = *(_WORD *)(a1 + 166) & 0xFFFE;
        v8 = (unsigned __int8)v8;
      }
      else
      {
        if ( a2 == 1145392197 )
        {
          sub_14118A970(a1);
          goto LABEL_171;
        }
        if ( a2 == 1148150639 )
        {
          v13 = sub_140DBC940();
          sub_140DBCA60(v13, &v45, v3);
          *(_DWORD *)(a1 + 48) = v45;
          goto LABEL_171;
        }
        if ( a2 != 1316316006 )
          return sub_140FE2700((_DWORD *)a1, a2, a3);
        v6 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 48))(*a3, a3);
        v7 = *(_WORD *)(a1 + 166) & 0xFF7F;
        v8 = v6 << 7;
      }
      goto LABEL_106;
    }
    if ( a2 > 1399087463 )
    {
      if ( a2 != 1399087464 )
      {
        if ( a2 == 1399087993 )
        {
          *(_BYTE *)(a1 + 154) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
          goto LABEL_171;
        }
        if ( a2 != 1399092338 )
          return sub_140FE2700((_DWORD *)a1, a2, a3);
        *(_BYTE *)(a1 + 156) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
        goto LABEL_171;
      }
      v28 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 48))(*a3, a3);
      v29 = *(_BYTE *)(a1 + 155);
      if ( v28 != 0 )
        v9 = v29 | 0x40;
      else
        v9 = v29 & 0xBF;
      goto LABEL_158;
    }
    if ( a2 == 1399025763 )
    {
      v45 = a1;
      sub_1415E6D60(v46, a1);
      v47 = &v45;
      v48 = v46;
      LODWORD(v3) = sub_14118D3D0(&v47, v3);
      if ( v46[0] != 0 )
        sub_1407E4890(qword_141ABD470, v46[0], v46[2] - v46[0]);
      return (unsigned int)v3;
    }
    if ( a2 != 1399025785 )
    {
      if ( a2 != 1399026793 )
        return sub_140FE2700((_DWORD *)a1, a2, a3);
      sub_140FE7E60(a1 + 80, a3);
      goto LABEL_171;
    }
    *(_DWORD *)(a1 + 108) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
    goto LABEL_112;
  }
  if ( a2 <= 1400009317 )
  {
    if ( a2 > 1399876717 )
    {
      if ( a2 > 1399878754 )
      {
        if ( a2 <= 1399879523 )
        {
          if ( a2 == 1399878755 )
          {
            *(_WORD *)(a1 + 152) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
            goto LABEL_171;
          }
          if ( a2 != 1399878777 )
            return sub_140FE2700((_DWORD *)a1, a2, a3);
          goto LABEL_92;
        }
        if ( a2 != 1399879524 )
        {
          if ( a2 == 1400005220 )
          {
            v11 = sub_140DBC940();
            sub_140DBCA60(v11, &v45, v3);
            *(_DWORD *)(a1 + 44) = v45;
            goto LABEL_171;
          }
          return sub_140FE2700((_DWORD *)a1, a2, a3);
        }
        v30 = sub_140FE8230();
        if ( v30 == 0 || *(_BYTE *)(v30 + 47) != 1 )
        {
          *(_WORD *)(a1 + 138) = (int)(float)(fminf(
                                                fmaxf(
                                                  (*(float (__fastcall **)(__int64 *, __int64 **))(**v3 + 96))(*v3, v3),
                                                  MEMORY[0x14187DC74]),
                                                MEMORY[0x14179E5F0])
                                            * MEMORY[0x141775530]);
          goto LABEL_171;
        }
        goto LABEL_153;
      }
      if ( a2 != 1399876718 )
      {
        if ( a2 == 1399878252 )
        {
          v18 = sub_140DBC940();
          sub_140DBCA60(v18, &v45, v3);
          *(_DWORD *)(a1 + 36) = v45;
          goto LABEL_171;
        }
        if ( a2 != 1399878258 )
          return sub_140FE2700((_DWORD *)a1, a2, a3);
        *(_BYTE *)(a1 + 158) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
LABEL_171:
        LOBYTE(v3) = 1;
        return (unsigned int)v3;
      }
      v17 = sub_140FE8230();
      if ( v17 == 0 || *(_BYTE *)(v17 + 47) != 1 )
      {
        *(_WORD *)(a1 + 136) = (int)(float)(fminf(
                                              fmaxf(
                                                (*(float (__fastcall **)(__int64 *, __int64 **))(**v3 + 96))(*v3, v3),
                                                MEMORY[0x14179E5F0]),
                                              MEMORY[0x1417B609C])
                                          * MEMORY[0x141775530]);
        goto LABEL_171;
      }
      goto LABEL_134;
    }
    if ( a2 <= 1399813739 )
    {
      switch ( a2 )
      {
        case 1399743863:
          LOBYTE(v3) = 1;
          if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 48))(*a3, a3) != 0 )
            *(_BYTE *)(a1 + 166) |= 0x10u;
          return (unsigned int)v3;
        case 1399744116:
          *(_BYTE *)(a1 + 165) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
          goto LABEL_171;
        case 1399813241:
          if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) != 0 )
            *(_BYTE *)(a1 + 164) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**v3 + 64))(*v3, v3);
          else
            *(_BYTE *)(a1 + 164) = 0;
          goto LABEL_171;
        default:
          break;
      }
      return sub_140FE2700((_DWORD *)a1, a2, a3);
    }
    if ( a2 != 1399813740 )
    {
      if ( a2 == 1399813993 )
      {
        sub_140FE7DE0(a1 + 128, a3);
        goto LABEL_171;
      }
      if ( a2 != 1399876690 )
        return sub_140FE2700((_DWORD *)a1, a2, a3);
      v10 = sub_140DBC940();
      sub_140DBCA60(v10, &v45, v3);
      *(_DWORD *)(a1 + 32) = v45;
      goto LABEL_171;
    }
    v21 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 48))(*a3, a3);
    v22 = *(_BYTE *)(a1 + 155);
    if ( v21 != 0 )
      v9 = v22 | 0x20;
    else
      v9 = v22 & 0xDF;
    goto LABEL_158;
  }
  if ( a2 > 1400189240 )
  {
    if ( a2 > 1400204915 )
    {
      if ( a2 <= 1400326476 )
      {
        if ( a2 == 1400204916 )
        {
          *(_BYTE *)(a1 + 161) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
          goto LABEL_171;
        }
        if ( a2 != 1400206184 )
          return sub_140FE2700((_DWORD *)a1, a2, a3);
        v5 = (*(_WORD *)(a1 + 166) & 0xFFFD)
           + 2 * (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 48))(*a3, a3);
LABEL_107:
        *(_WORD *)(a1 + 166) = v5;
        goto LABEL_171;
      }
      if ( a2 == 1400326477 )
      {
        if ( (*(unsigned __int8 (__fastcall **)(__int64 *, __int64 **))(**a3 + 8))(*a3, a3) == 0 )
        {
          *(_WORD *)(a1 + 142) = -1;
          goto LABEL_171;
        }
        if ( (*(int (__fastcall **)(__int64 *, __int64 **))(**v3 + 64))(*v3, v3) <= 0 )
        {
          v37.m128_f32[0] = (float)*(__int16 *)(a1 + 138) / MEMORY[0x141775530];
          v44 = _mm_cmpge_ss((__m128)MEMORY[0x141759000], v37);
          v37.m128_f32[0] = fminf(fmaxf(v37.m128_f32[0], MEMORY[0x14187DC74]), MEMORY[0x14179E5F0])
                          * MEMORY[0x141775530];
          v41 = (int)COERCE_FLOAT(MEMORY[0x1417E35FC] & v44.m128_i32[0] | _mm_andnot_ps(v44, v37).m128_u32[0]);
          goto LABEL_170;
        }
LABEL_153:
        *(double *)v38.m128_u64 = (*(double (__fastcall **)(__int64 *, __int64 **))(**v3 + 96))(*v3, v3);
        v39 = v38;
        v40 = _mm_cmpge_ss((__m128)MEMORY[0x141759000], v38);
        v39.m128_f32[0] = fminf(fmaxf(v38.m128_f32[0], MEMORY[0x14187DC74]), MEMORY[0x14179E5F0]) * MEMORY[0x141775530];
        v41 = (int)COERCE_FLOAT(MEMORY[0x1417E35FC] & v40.m128_i32[0] | _mm_andnot_ps(v40, v39).m128_u32[0]);
LABEL_170:
        *(_WORD *)(a1 + 142) = v41;
        goto LABEL_171;
      }
      if ( a2 != 1467310950 )
        return sub_140FE2700((_DWORD *)a1, a2, a3);
      v12 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 48))(*a3, a3);
      v7 = *(_WORD *)(a1 + 166) & 0xF7FF;
      v8 = v12 << 11;
LABEL_106:
      v5 = v7 | v8;
      goto LABEL_107;
    }
    if ( a2 == 1400189241 )
    {
      *(_BYTE *)(a1 + 163) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
      goto LABEL_171;
    }
    if ( a2 == 1400189489 )
    {
      *(_BYTE *)(a1 + 162) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
      goto LABEL_171;
    }
    if ( a2 != 1400202105 )
      return sub_140FE2700((_DWORD *)a1, a2, a3);
    *(_DWORD *)(a1 + 116) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
    goto LABEL_112;
  }
  if ( a2 <= 1400071282 )
  {
    if ( a2 == 1400009318 )
    {
      v14 = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 48))(*a3, a3);
      v7 = *(_WORD *)(a1 + 166) & 0xFFBF;
      v8 = v14 << 6;
      goto LABEL_106;
    }
    if ( a2 == 1400071020 )
    {
      v15 = sub_141335F60();
      sub_1413360C0(v15, &v45, v3);
      *(_DWORD *)(a1 + 104) = v45;
      goto LABEL_171;
    }
    if ( a2 != 1400071033 )
      return sub_140FE2700((_DWORD *)a1, a2, a3);
    *(_DWORD *)(a1 + 112) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
LABEL_112:
    v16 = *(_QWORD *)(a1 + 24);
    LOBYTE(v3) = 1;
    if ( v16 != 0 && *(_BYTE *)(v16 + 64) != 0 )
      sub_14118AF00(a1);
    return (unsigned int)v3;
  }
  if ( a2 == 1400071283 )
  {
    sub_1415E7F10(&v45, a1);
    v47 = &v45;
    v48 = &v45;
    LODWORD(v3) = sub_14118CE50(&v47, v3);
    sub_14093AAF0(&v45);
    return (unsigned int)v3;
  }
  if ( a2 != 1400071764 )
  {
    if ( a2 != 1400075365 )
      return sub_140FE2700((_DWORD *)a1, a2, a3);
    *(_BYTE *)(a1 + 159) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3);
    goto LABEL_171;
  }
LABEL_92:
  if ( (*(unsigned int (__fastcall **)(__int64 *, __int64 **))(**a3 + 64))(*a3, a3) <= 8 )
  {
    *(_BYTE *)(a1 + 157) = (*(__int64 (__fastcall **)(__int64 *, __int64 **))(**v3 + 64))(*v3, v3);
    goto LABEL_171;
  }
  LODWORD(v3) = 0;
  return (unsigned int)v3;
}
