char __fastcall sub_140DC3790(__int64 a1)
{
  __int64 v2; // r8
  unsigned __int64 v3; // rdi
  char v4; // cl
  float v5; // xmm0_4
  int v6; // eax
  float v7; // xmm1_4
  char v8; // cl
  unsigned __int64 v9; // rax
  char *v10; // rdx
  int v11; // ebp
  char v12; // cl
  float v13; // xmm0_4
  float v14; // xmm0_4
  int v15; // eax
  float v16; // xmm0_4
  char v17; // cl
  int v18; // eax
  float v19; // xmm0_4
  char v20; // cl
  int v21; // eax
  float v22; // xmm0_4
  char v23; // cl
  int v24; // eax
  float v25; // xmm0_4
  char v26; // cl
  char v27; // al
  unsigned int v28; // ebx
  unsigned __int64 v29; // rbx
  char v30; // al
  int v31; // eax
  __int64 v32; // rdi
  float v33; // xmm0_4
  char v34; // al
  unsigned int v35; // ebp
  char v36; // cl
  unsigned __int64 v37; // rdi
  unsigned int v38; // eax
  unsigned __int64 v39; // rdi
  __int64 v40; // rax
  __int64 v41; // rax
  __int64 v42; // rcx
  unsigned __int8 v43; // al
  unsigned int v44; // ecx
  int v45; // ebp
  unsigned __int64 v46; // rbp
  __int64 v47; // rbx
  __int64 v48; // rcx
  int v49; // ebp
  unsigned __int8 v50; // al
  unsigned int v51; // ecx
  int v52; // edx
  unsigned __int64 v53; // rdx
  __int64 v54; // rbx
  unsigned __int64 v55; // rcx
  __int64 v56; // rax
  __int64 *v57; // rax
  __int64 v58; // rcx
  unsigned int v59; // eax
  unsigned __int16 v60; // cx

  v2 = *(_QWORD *)(a1 + 8);
  v3 = 0xA4E7735A4C957F2DuLL * *(unsigned int *)(*(int *)(v2 + 4) + a1 + 20) + 0x5851F42D4C957F2ELL;
  if ( *(_BYTE *)(a1 + 229) == 2 )
  {
    v13 = (float)(int)__ROR4__((v3 >> 27) ^ (v3 >> 45), v3 >> 59) * MEMORY[0x14179AD28];
    v3 = 0x5851F42D4C957F2DLL * v3 + 1;
    *(_BYTE *)(a1 + 229) = MEMORY[0x1417B6094] < v13;
    if ( *(_BYTE *)(a1 + 230) != 3 )
    {
LABEL_3:
      if ( *(_BYTE *)(a1 + 231) != 3 )
        goto LABEL_4;
      goto LABEL_19;
    }
  }
  else if ( *(_BYTE *)(a1 + 230) != 3 )
  {
    goto LABEL_3;
  }
  v14 = (float)(int)__ROR4__((v3 >> 27) ^ (v3 >> 45), v3 >> 59) * MEMORY[0x14179AD28];
  v3 = 0x5851F42D4C957F2DLL * v3 + 1;
  *(_BYTE *)(a1 + 230) = MEMORY[0x141774E1C] < v14;
  if ( *(_BYTE *)(a1 + 231) != 3 )
  {
LABEL_4:
    if ( *(_BYTE *)(a1 + 232) != 3 )
      goto LABEL_5;
    goto LABEL_22;
  }
LABEL_19:
  v15 = __ROR4__((v3 >> 27) ^ (v3 >> 45), v3 >> 59);
  v3 = 0x5851F42D4C957F2DLL * v3 + 1;
  v16 = (float)v15 * MEMORY[0x14179AD28];
  v17 = (MEMORY[0x141876F20] < v16) + 1;
  if ( MEMORY[0x141764680] >= v16 )
    v17 = 0;
  *(_BYTE *)(a1 + 231) = v17;
  if ( *(_BYTE *)(a1 + 232) != 3 )
  {
LABEL_5:
    if ( *(_BYTE *)(a1 + 233) != 3 )
      goto LABEL_6;
    goto LABEL_25;
  }
LABEL_22:
  v18 = __ROR4__((v3 >> 27) ^ (v3 >> 45), v3 >> 59);
  v3 = 0x5851F42D4C957F2DLL * v3 + 1;
  v19 = (float)v18 * MEMORY[0x14179AD28];
  v20 = (MEMORY[0x141764688] < v19) + 1;
  if ( MEMORY[0x141764684] >= v19 )
    v20 = 0;
  *(_BYTE *)(a1 + 232) = v20;
  if ( *(_BYTE *)(a1 + 233) != 3 )
  {
LABEL_6:
    if ( *(_BYTE *)(a1 + 234) != 3 )
      goto LABEL_7;
    goto LABEL_28;
  }
LABEL_25:
  v21 = __ROR4__((v3 >> 27) ^ (v3 >> 45), v3 >> 59);
  v3 = 0x5851F42D4C957F2DLL * v3 + 1;
  v22 = (float)v21 * MEMORY[0x14179AD28];
  v23 = (MEMORY[0x141876F24] < v22) + 1;
  if ( MEMORY[0x141774E1C] >= v22 )
    v23 = 0;
  *(_BYTE *)(a1 + 233) = v23;
  if ( *(_BYTE *)(a1 + 234) != 3 )
  {
LABEL_7:
    if ( *(_BYTE *)(a1 + 235) != 3 )
      goto LABEL_13;
    goto LABEL_8;
  }
LABEL_28:
  v24 = __ROR4__((v3 >> 27) ^ (v3 >> 45), v3 >> 59);
  v3 = 0x5851F42D4C957F2DLL * v3 + 1;
  v25 = (float)v24 * MEMORY[0x14179AD28];
  v26 = (MEMORY[0x141876F24] < v25) + 1;
  if ( MEMORY[0x1417B6094] >= v25 )
    v26 = 0;
  *(_BYTE *)(a1 + 234) = v26;
  if ( *(_BYTE *)(a1 + 235) == 3 )
  {
LABEL_8:
    v4 = 10;
    if ( *(_BYTE *)(a1 + 43) != 0 )
      v4 = *(_BYTE *)(a1 + 43);
    v5 = (float)((float)(v4 - 10) / MEMORY[0x141876F28]) + MEMORY[0x141774E1C];
    v6 = __ROR4__((v3 >> 27) ^ (v3 >> 45), v3 >> 59);
    v3 = 0x5851F42D4C957F2DLL * v3 + 1;
    v7 = (float)v6 * MEMORY[0x14179AD28];
    v8 = ((float)(MEMORY[0x141764680] + v5) < v7) + 1;
    if ( v5 >= v7 )
      v8 = 0;
    *(_BYTE *)(a1 + 235) = v8;
  }
LABEL_13:
  v9 = *(int *)(v2 + 8);
  v10 = *(char **)(v9 + a1 + 224);
  if ( v10 == nullptr )
  {
    if ( *(_BYTE *)(a1 + 75) != 0 )
      return v9;
    goto LABEL_51;
  }
  v11 = (int)(float)((float)((float)((float)((float)((float)((float)*(__int16 *)(a1 + 214) / MEMORY[0x141775564])
                                                   + MEMORY[0x141775558])
                                           + MEMORY[0x141759000])
                                   * MEMORY[0x141876F2C])
                           / MEMORY[0x141876F30])
                   + MEMORY[0x1417597F0]);
  if ( v10[2] <= 17 )
  {
    v27 = v10[1];
    v12 = *(_BYTE *)(a1 + 75);
    if ( v12 != 0 )
    {
      if ( v27 < 18 )
        goto LABEL_54;
      goto LABEL_43;
    }
    if ( v27 >= 18 )
      goto LABEL_38;
LABEL_51:
    v35 = __ROR4__((v3 >> 27) ^ (v3 >> 45), v3 >> 59);
    v3 = 0x5851F42D4C957F2DLL * v3 + 1;
    LOBYTE(v9) = (char)((10923
                       * (__int16)(*(char *)(a1 + 58)
                                 + *(char *)(a1 + 59)
                                 + *(char *)(a1 + 60)
                                 + *(char *)(a1 + 61)
                                 + *(char *)(a1 + 63)
                                 + *(char *)(a1 + 62)) < 0)
                      + ((unsigned int)(10923
                                      * (__int16)(*(char *)(a1 + 58)
                                                + *(char *)(a1 + 59)
                                                + *(char *)(a1 + 60)
                                                + *(char *)(a1 + 61)
                                                + *(char *)(a1 + 63)
                                                + *(char *)(a1 + 62))) >> 16))
               / (char)(((((3 * (unsigned __int64)v35) >> 8) & 0x3000000) + 0x2000000) >> 24);
    v36 = 1;
    if ( (char)v9 >= 2 )
      v36 = (char)((10923
                  * (__int16)(*(char *)(a1 + 58)
                            + *(char *)(a1 + 59)
                            + *(char *)(a1 + 60)
                            + *(char *)(a1 + 61)
                            + *(char *)(a1 + 63)
                            + *(char *)(a1 + 62)) < 0)
                 + ((unsigned int)(10923
                                 * (__int16)(*(char *)(a1 + 58)
                                           + *(char *)(a1 + 59)
                                           + *(char *)(a1 + 60)
                                           + *(char *)(a1 + 61)
                                           + *(char *)(a1 + 63)
                                           + *(char *)(a1 + 62))) >> 16))
          / (char)(((((3 * (unsigned __int64)v35) >> 8) & 0x3000000) + 0x2000000) >> 24);
    *(_BYTE *)(a1 + 75) = v36;
    if ( v10 == nullptr )
      return v9;
    goto LABEL_54;
  }
  v12 = *(_BYTE *)(a1 + 75);
  if ( v12 == 0 )
  {
LABEL_38:
    v28 = __ROR4__((v3 >> 27) ^ (v3 >> 45), v3 >> 59);
    v3 = 0x5851F42D4C957F2DLL * v3 + 1;
    v29 = (((char)v11 + 1LL) * (unsigned __int64)v28) >> 32;
    v30 = 1;
    if ( (char)v29 >= 2 )
      v30 = v29;
    v12 = 100;
    if ( v30 < 100 )
      v12 = v30;
    *(_BYTE *)(a1 + 75) = v12;
  }
LABEL_43:
  if ( (float)((float)v12 / (float)(char)v11) >= MEMORY[0x141764690] )
  {
    v31 = __ROR4__((v3 >> 27) ^ (v3 >> 45), v3 >> 59);
    v32 = 0x5851F42D4C957F2DLL * v3;
    v33 = (float)v31 * MEMORY[0x14179AD28];
    v34 = 18;
    if ( MEMORY[0x14177801C] < v33 )
    {
      v34 = 15;
      if ( MEMORY[0x141876F34] < v33 )
      {
        v34 = 12;
        if ( MEMORY[0x141876F38] < v33 )
        {
          v34 = 1;
          if ( MEMORY[0x141876F3C] >= v33 )
            v34 = 5 * ((*(_BYTE *)(*(int *)(v2 + 4) + a1 + 20) & 1) == 0) + 5;
        }
      }
    }
    v3 = v32 + 1;
    v10[7] = v34;
    v2 = *(_QWORD *)(a1 + 8);
  }
LABEL_54:
  v9 = *(_QWORD *)(*(int *)(v2 + 4) + a1 + 32) & 8LL;
  if ( (*(_QWORD *)(*(int *)(v2 + 4) + a1 + 32) & 8) != 0 && *v10 >= 11 )
  {
    v9 = (100 * (unsigned __int64)(unsigned int)__ROR4__((v3 >> 27) ^ (v3 >> 45), v3 >> 59)) >> 32;
    if ( (unsigned int)v9 <= 0xA )
    {
      v37 = 0x5851F42D4C957F2DLL * v3 + 1;
      v38 = __ROR4__((v37 >> 27) ^ (v37 >> 45), v37 >> 59);
      v39 = 0x5851F42D4C957F2DLL * v37 + 1;
      if ( (10 * (unsigned __int64)v38) >> 32 != 0 )
      {
        v41 = *(int *)(v2 + 8);
        v42 = *(_QWORD *)(v41 + a1 + 168);
        if ( v42 == 0 )
        {
          v57 = *(__int64 **)(a1 + v41 + 176);
          if ( v57 == nullptr )
            goto LABEL_81;
          v42 = *v57;
          if ( *v57 == 0 )
            goto LABEL_81;
        }
        v43 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v42 + 80LL))(a1: v42);
        v44 = v43 & 0xFE;
        if ( (v43 & 0xFEu) > 0x18 || (v45 = 16777296, !_bittest(&v45, v44)) )
        {
          if ( v44 != 70 && v44 != 84 )
          {
            v46 = (unsigned int)v43 - 8;
            if ( (unsigned int)v46 > 0x3B || (v47 = 0xC00000000000003LL, !_bittest64(&v47, v46)) )
            {
              if ( (v43 & 0xF6) != 0x26 && (v43 & 0xFE) != 0x44 && v44 != 28 )
                goto LABEL_81;
            }
          }
        }
        v48 = *(_QWORD *)(*(int *)(*(_QWORD *)(a1 + 8) + 8LL) + a1 + 168);
        v49 = 101;
        if ( v48 != 0 )
        {
          v50 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v48 + 104LL))(a1: v48);
          if ( v50 != 0 )
          {
            v51 = v50 & 0xFE;
            if ( (unsigned __int8)v51 > 0x18u || (v52 = 16777296, !_bittest(&v52, v51)) )
            {
              if ( v51 != 70 && v51 != 84 )
              {
                v53 = (unsigned int)v50 - 8;
                if ( (unsigned int)v53 > 0x3B || (v54 = 0xC00000000000003LL, !_bittest64(&v54, v53)) )
                {
                  if ( (v50 & 0xF6) != 0x26 )
                  {
                    v55 = (unsigned int)v50 - 28;
                    if ( (unsigned int)v55 > 0x29 || (v56 = 0x30000000003LL, !_bittest64(&v56, v55)) )
                    {
LABEL_81:
                      v58 = a1 + *(int *)(*(_QWORD *)(a1 + 8) + 4LL) + 8;
                      if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v58 + 528LL))(a1: v58) == 0
                        || (v49 = 101, (unsigned __int8)sub_1400015B0() == 0) )
                      {
                        v49 = (char)(101 - *(_BYTE *)(a1 + 75));
                      }
                    }
                  }
                }
              }
            }
          }
        }
        v59 = __ROR4__(
                ((0x5851F42D4C957F2DLL * v39 + 1) >> 27) ^ ((0x5851F42D4C957F2DLL * v39 + 1) >> 45),
                (0x5851F42D4C957F2DLL * v39 + 1) >> 59);
        if ( v49 >= (int)((100 * (unsigned __int64)(unsigned int)__ROR4__((v39 >> 27) ^ (v39 >> 45), v39 >> 59)) >> 32) )
        {
          v40 = 11LL * v59;
          v60 = 10;
          goto LABEL_88;
        }
        v40 = 9LL * v59;
      }
      else
      {
        v40 = 20LL * (unsigned int)__ROR4__((v39 >> 27) ^ (v39 >> 45), v39 >> 59);
      }
      v60 = 1;
LABEL_88:
      LOBYTE(v9) = sub_140DC5A10(a1, a2: ((HIDWORD(v40) + v60) << 8) | 0x60u);
    }
  }
  return v9;
}
