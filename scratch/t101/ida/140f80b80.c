__int64 __fastcall sub_140F80B80(__int64 *a1, _QWORD *a2, int a3)
{
  __int64 v3; // rbp
  _DWORD *v6; // rdi
  _DWORD *v7; // rdi
  int v8; // eax
  __int64 v9; // rdi
  int v10; // eax
  __int64 v11; // rdi
  _QWORD *v12; // rdx
  char v13; // cl
  __int64 v14; // r8
  char v15; // al
  __int64 v16; // rdi
  __int64 v17; // rcx
  __int64 v18; // rcx
  __int64 v20; // rdi
  __int64 v21; // rdi
  __int64 v22; // rdi
  char v23; // al
  __int64 v24; // rdi
  __int64 v25; // rdi
  __int64 v26; // rdi
  __int16 v27; // ax
  unsigned __int64 v28; // rbx
  __int64 v29; // rcx
  __int64 v30; // rcx
  __int64 v31; // rax
  unsigned int v32; // ecx
  __int64 v33; // rcx
  __int64 *v34; // rdx
  unsigned __int64 v35; // r8
  __int64 v36; // rax
  __int64 v37; // rdi
  __int64 **v38; // rdx
  __int64 *v39; // rax
  __int64 *v40; // rdx
  __int64 v41; // rbx
  char v42; // r8
  __int64 v43; // rdi
  __int64 v44; // r8
  char v45; // al
  char v46; // [rsp+31h] [rbp-57h] BYREF
  char v47; // [rsp+32h] [rbp-56h] BYREF
  char v48; // [rsp+33h] [rbp-55h] BYREF
  __int16 v49; // [rsp+34h] [rbp-54h] BYREF
  char v50; // [rsp+36h] [rbp-52h] BYREF
  char v51; // [rsp+37h] [rbp-51h] BYREF
  unsigned int v52; // [rsp+38h] [rbp-50h] BYREF
  char v53; // [rsp+3Fh] [rbp-49h] BYREF
  int v54; // [rsp+40h] [rbp-48h] BYREF
  __int64 v55; // [rsp+48h] [rbp-40h] BYREF
  __int64 v56; // [rsp+50h] [rbp-38h] BYREF
  __int64 v57; // [rsp+58h] [rbp-30h] BYREF
  _QWORD v58[5]; // [rsp+60h] [rbp-28h] BYREF

  v6 = (_DWORD *)*a2;
  if ( (*(_BYTE *)(*a2 + 12LL) & 2) != 0 )
  {
    v13 = HIBYTE(qword_141B6034C);
    if ( BYTE6(qword_141B6034C) != 0 || a3 == 1 && (v13 = 1, HIBYTE(qword_141B6034C) != 0) )
    {
      if ( v13 == 0 || byte_141B5FC2C != 0 )
        v14 = 4;
      else
        v14 = 8;
      (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)v6 + 40LL))(*a2, a1, v14);
      if ( v6[4] != 0 )
        goto LABEL_32;
LABEL_33:
      LOBYTE(v3) = 1;
      return (unsigned int)v3;
    }
  }
  *a1 = 0;
  v7 = (_DWORD *)*a2;
  v8 = *(_DWORD *)(*a2 + 12LL);
  if ( (v8 & 2) != 0 )
  {
    v15 = (2 * ~(_BYTE)v8) & 4;
    if ( byte_141AAE088 == 0 )
      v15 = 0;
    v50 = v15;
    if ( v15 == 0 )
      goto LABEL_5;
  }
  else
  {
    (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)v7 + 40LL))(*a2, &v50, 1);
    if ( v7[4] != 0 )
      goto LABEL_32;
    if ( v50 == 0 )
    {
LABEL_5:
      v3 = qword_141B5FDC0;
      *a1 = 0;
      v9 = *a2;
      (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v56, 2);
      if ( *(_DWORD *)(v9 + 16) == 0 )
      {
        v10 = (__int16)v56;
        if ( (__int16)v56 == -1 )
          goto LABEL_33;
        LODWORD(v55) = (__int16)v56;
        if ( (_WORD)v56 == 0xFFFE )
        {
          v11 = *a2;
          (*(void (__fastcall **)(_QWORD, __int64 *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v55, 4);
          if ( *(_DWORD *)(v11 + 16) != 0 )
            goto LABEL_32;
          v10 = v55;
        }
        if ( v10 >= 0 )
        {
          v12 = *(_QWORD **)(v3 + 128);
          if ( (__int64)(v12[1] - *v12) >> 3 > (unsigned __int64)(unsigned int)v10 )
          {
            *a1 = *(_QWORD *)(*v12 + 8LL * (unsigned int)v10);
            goto LABEL_33;
          }
        }
      }
LABEL_32:
      LODWORD(v3) = 0;
      return (unsigned int)v3;
    }
  }
  v52 = -1;
  v55 = 0;
  v56 = 0;
  v58[0] = 0;
  v57 = 0;
  v48 = 0;
  v47 = 1;
  *a1 = 0;
  v16 = *a2;
  (*(void (__fastcall **)(_QWORD, __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v49, 2);
  if ( *(_DWORD *)(v16 + 16) != 0 )
    goto LABEL_23;
  LOBYTE(v3) = 1;
  if ( v49 == -1 )
    goto LABEL_24;
  v20 = *a2;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v46, 1);
  if ( *(_DWORD *)(v20 + 16) != 0 )
    goto LABEL_23;
  v21 = *a2;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v51, 1);
  if ( *(_DWORD *)(v21 + 16) != 0 )
    goto LABEL_23;
  v22 = *a2;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v53, 1);
  if ( *(_DWORD *)(v22 + 16) != 0 )
    goto LABEL_23;
  if ( v53 == 0 )
  {
    v36 = sub_140F45D40((unsigned int)v49);
    *a1 = v36;
    LOBYTE(v3) = v36 != 0;
    goto LABEL_24;
  }
  v23 = v46;
  if ( v46 > 0 )
  {
    v24 = *a2;
    (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v52, 4);
    if ( *(_DWORD *)(v24 + 16) == 0
      && (unsigned __int8)sub_140F92E30(
                            (unsigned int)&qword_141B5FDA8,
                            (unsigned int)&v55,
                            (_DWORD)a2,
                            qword_141B5FDD0,
                            (unsigned __int8)byte_141B5FC2C ^ 1u) != 0
      && (unsigned __int8)sub_140F92AB0(
                            (unsigned int)&qword_141B5FDA8,
                            (unsigned int)&v56,
                            (_DWORD)a2,
                            qword_141B5FDC8,
                            (unsigned __int8)byte_141B5FC2C ^ 1u) != 0 )
    {
      v25 = *a2;
      (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v48, 1);
      if ( *(_DWORD *)(v25 + 16) == 0 )
      {
        v23 = v46;
        if ( v46 != 4 )
          goto LABEL_49;
        sub_140814B10(*a2, &v54, v58);
        if ( v54 == 0 )
        {
          sub_140814B10(*a2, &v54, &v57);
          if ( v54 == 0 )
          {
            v23 = v46;
            goto LABEL_49;
          }
        }
      }
    }
LABEL_23:
    LODWORD(v3) = 0;
    goto LABEL_24;
  }
LABEL_49:
  if ( v23 == 0 )
  {
    v37 = *a2;
    (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v52, 4);
    if ( *(_DWORD *)(v37 + 16) != 0 )
      goto LABEL_23;
  }
  v26 = *a2;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v47, 1);
  if ( *(_DWORD *)(v26 + 16) != 0 )
    goto LABEL_23;
  v27 = v49;
  v28 = v49;
  if ( (_BYTE)word_141B60320 != 0
    || (v29 = *(_QWORD *)(qword_141B5FDC0 + 96), (*(_QWORD *)(qword_141B5FDC0 + 104) - v29) >> 3 <= (unsigned __int64)v49)
    || (v30 = *(_QWORD *)(v29 + 8LL * v49), *a1 = v30, v30 == 0)
    || *(_DWORD *)(v30 + 12) != v52 && v52 != -1 )
  {
    if ( (__int64)(*(_QWORD *)(*(_QWORD *)(qword_141B5FDC0 + 128) + 8LL) - **(_QWORD **)(qword_141B5FDC0 + 128)) >> 3 <= v28 )
    {
      *a1 = 0;
      v32 = v52;
      if ( v52 == -1 )
        goto LABEL_24;
    }
    else
    {
      v31 = sub_140F45D40((unsigned int)v27);
      *a1 = v31;
      v32 = v52;
      if ( v52 == -1 || v31 != 0 && *(_DWORD *)(v31 + 12) == v52 )
      {
        if ( v31 == 0 || (_BYTE)word_141B60320 != 0 )
          goto LABEL_24;
        *(_BYTE *)(v31 + 417) = *(_BYTE *)(v31 + 417) & 0xEF | (16 * v47);
        v33 = qword_141B5FDC0 + 96;
        v34 = a1;
        v35 = v28;
        goto LABEL_83;
      }
    }
    *a1 = 0;
    v38 = *(__int64 ***)(qword_141B5FDC0 + 128);
    v39 = *v38;
    v40 = v38[1];
    while ( v39 != v40 )
    {
      v41 = *v39;
      if ( *v39 != 0 && *(_DWORD *)(v41 + 12) == v32 )
      {
        *a1 = v41;
        v42 = v46;
        *(_BYTE *)(v41 + 416) = v46;
        *(_BYTE *)(*a1 + 244) = v51;
        *(_BYTE *)(*a1 + 417) = *(_BYTE *)(*a1 + 417) & 0xEF | (16 * v47);
        if ( v42 <= 0 )
        {
LABEL_75:
          if ( v42 == 0 )
            *(_DWORD *)(*a1 + 12) = v52;
        }
        else
        {
          *(_DWORD *)(*a1 + 12) = v32;
          *(_QWORD *)(*a1 + 96) = v55;
          *(_QWORD *)(*a1 + 88) = v56;
          *(_BYTE *)(*a1 + 418) = v48;
          if ( v42 == 4 )
          {
            sub_140809100(*a1 + 64, v58);
            sub_140809100(*a1 + 72, &v57);
            v42 = v46;
            goto LABEL_75;
          }
        }
        if ( (_BYTE)word_141B60320 == 0 )
        {
          sub_14083D020(qword_141B5FDC0 + 96, a1, v49);
          *(_DWORD *)(*a1 + 8) = v49;
        }
        goto LABEL_24;
      }
      ++v39;
    }
    if ( (_BYTE)word_141B60320 != 0 )
      goto LABEL_23;
    v43 = sub_140F6EAE0(432);
    sub_140EB6A10(v43, v52);
    *a1 = v43;
    *(_QWORD *)(v43 + 96) = v55;
    *(_QWORD *)(*a1 + 88) = v56;
    v45 = v46;
    *(_BYTE *)(*a1 + 416) = v46;
    *(_BYTE *)(*a1 + 244) = v51;
    *(_BYTE *)(*a1 + 418) = v48;
    if ( v45 == 4 )
    {
      sub_140809100(*a1 + 64, v58);
      sub_140809100(*a1 + 72, &v57);
    }
    LOBYTE(v3) = 1;
    LOBYTE(v44) = 1;
    sub_140F6C770(qword_141B5FDC0, *a1, v44);
    v35 = v49;
    *(_DWORD *)(*a1 + 8) = v49;
    v33 = qword_141B5FDC0 + 96;
    v34 = a1;
LABEL_83:
    sub_14083D020(v33, v34, v35);
    goto LABEL_24;
  }
  *(_BYTE *)(v30 + 417) = *(_BYTE *)(v30 + 417) & 0xEF | (16 * v47);
LABEL_24:
  v17 = v57;
  if ( v57 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v57 - 4)) == 0 )
    sub_1412EC9A0(v17 - 4);
  v18 = v58[0];
  if ( v58[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v58[0] - 4LL)) == 0 )
    sub_1412EC9A0(v18 - 4);
  return (unsigned int)v3;
}
