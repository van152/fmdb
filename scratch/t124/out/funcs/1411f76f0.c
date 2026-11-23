__int64 __fastcall sub_1411F76F0(__int64 a1, __int16 a2, unsigned int a3, _QWORD *a4)
{
  unsigned int v4; // r15d
  __int64 v7; // r10
  __int16 v8; // r8
  __int64 v9; // r9
  __int64 v10; // rsi
  __int64 v11; // rdi
  __int16 v12; // bx
  int v13; // eax
  __int64 v14; // rsi
  char v16; // al
  char v17; // cl
  char v18; // cl
  __int64 v19; // rax
  __int64 v20; // rbx
  __int64 v21; // rdx
  __int64 v22; // rcx
  __int64 v23; // r8
  __int64 v24; // r9
  __int64 v25; // rax
  __int64 v26; // rdx
  __int64 v27; // rcx
  __int64 v28; // r8
  __int64 v29; // r9
  __int64 v30; // rax
  __int64 v31; // rdx
  __int64 v32; // r8
  __int64 v33; // r9
  __int64 v34; // rcx
  __int64 v35; // rsi
  unsigned __int64 v36; // rsi
  __int64 v37; // rax
  __int64 v38; // rdx
  __int64 v39; // rcx
  __int64 v40; // r8
  __int64 v41; // r9
  __int64 v42; // rax
  __int64 v43; // rax
  __int64 v44; // rcx
  int v45; // esi
  __int64 *v46; // rax
  __int64 *v47; // rdi
  __int64 v48; // rdx
  __int64 v49; // rcx
  __int64 v50; // r8
  __int64 v51; // r9
  __int64 v52; // rax
  __int64 v53; // rdx
  __int64 v54; // rcx
  __int64 v55; // r8
  __int64 v56; // r9
  __int64 v57; // rax
  int v58; // r8d
  int v59; // r9d
  _BYTE v60[24]; // [rsp+60h] [rbp-20h] BYREF
  __int64 v61; // [rsp+78h] [rbp-8h] BYREF
  unsigned __int64 v62; // [rsp+80h] [rbp+0h]
  __int64 v63; // [rsp+88h] [rbp+8h]

  v63 = -2;
  v7 = *(_QWORD *)(a1 + 24);
  v8 = -1;
  v9 = *(_QWORD *)(a1 + 32) - v7;
  if ( v9 != 0 )
  {
    v10 = 1;
    if ( (unsigned __int64)(v9 >> 3) >= 2 )
      v10 = v9 >> 3;
    v11 = 0;
    v12 = 0;
    do
    {
      v13 = *(unsigned __int8 *)(*(_QWORD *)(v7 + 8 * v11) + 40LL);
      if ( v13 != 22 && v13 != 44 )
      {
        if ( v12 == a2 )
        {
          v8 = v11;
          break;
        }
        ++v12;
      }
      ++v11;
    }
    while ( v10 != v11 );
  }
  LOBYTE(v4) = 1;
  if ( (_BYTE)word_141B60320 == 0 )
    return v4;
  v14 = 0;
  if ( v8 >= 0 && (int)(((unsigned __int64)v9 >> 3) - 1) >= v8 )
    v14 = *(_QWORD *)(v7 + 8LL * (unsigned __int16)v8);
  if ( *(_BYTE *)(a1 + 186) != 0 )
    goto LABEL_16;
  if ( (int)a3 > 1416851040 )
  {
    if ( a3 != 1416851041 )
    {
      if ( a3 == 1684632417 )
      {
        if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)qword_141B5AD60 + 32LL))(a1: qword_141B5AD60) != 0
          && v14 != 0
          && (HIWORD(dword_141AAE084) ^ 0x76C | dword_141AAE084 & 0x1FF ^ 1) != 0 )
        {
          v16 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a4 + 48LL))(a1: *a4, a2: a4);
          v17 = *(_BYTE *)(v14 + 176) & 0x7E | 0x80;
          if ( v16 != 0 )
            v17 = *(_BYTE *)(v14 + 176) | 1;
          *(_BYTE *)(v14 + 176) = v17;
          if ( (v17 & 1) != 0 )
            v18 = v17 | 8;
          else
            v18 = v17 & 0xF3;
          *(_BYTE *)(v14 + 176) = v18;
        }
        return v4;
      }
      goto LABEL_16;
    }
  }
  else if ( a3 != 1131640942 && a3 != 1416392289 )
  {
LABEL_16:
    if ( v14 != 0 )
      return sub_1411B5630(a1: v14, a2: a3, a3: a4);
    return 0;
  }
  if ( v14 == 0 )
    return 0;
  if ( *(_DWORD *)(v14 + 12) == -1 )
    return sub_1411B5630(a1: v14, a2: a3, a3: a4);
  v19 = sub_140F45DB0(a1: qword_141B5FDB8);
  if ( v19 == 0 )
    return sub_1411B5630(a1: v14, a2: a3, a3: a4);
  v20 = v19;
  sub_1407C9510(a1: v60);
  v25 = sub_14083D4F0(a1: v22, a2: v21, a3: v23, a4: v24);
  LOBYTE(v62) = 1;
  v61 = v25 + 24;
  sub_140833EB0(a1: v60, a2: 1230195782, a3: &v61);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v61 + 16LL))(a1: v61, a2: &v61);
  v30 = sub_14083D4F0(a1: v27, a2: v26, a3: v28, a4: v29);
  LODWORD(v62) = 3;
  v61 = v30 + 40;
  sub_140833EB0(a1: v60, a2: 1685353593, a3: &v61);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v61 + 16LL))(a1: v61, a2: &v61);
  v34 = *(unsigned int *)(v20 + 16);
  v35 = *(unsigned int *)(v20 + 12);
  if ( (_DWORD)v34 != 0 )
    v35 = (unsigned int)v34;
  v36 = *(int *)(v20 + 12) | (unsigned __int64)(v35 << 32);
  v37 = sub_14083D4F0(a1: v34, a2: v31, a3: v32, a4: v33);
  v62 = v36;
  v61 = v37 + 72;
  sub_140833EB0(a1: v60, a2: 1685417577, a3: &v61);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v61 + 16LL))(a1: v61, a2: &v61);
  if ( a3 == 1416851041 )
  {
    v43 = sub_14083D4F0(a1: v39, a2: v38, a3: v40, a4: v41);
    LODWORD(v62) = 1131638381;
    v61 = v43 + 56;
    sub_140833EB0(a1: v60, a2: 1886549113, a3: &v61);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v61 + 16LL))(a1: v61, a2: &v61);
  }
  else
  {
    v42 = sub_14083D4F0(a1: v39, a2: v38, a3: v40, a4: v41);
    if ( a3 == 1416392289 )
      LODWORD(v62) = 1131307373;
    else
      LODWORD(v62) = 1131640942;
    v61 = v42 + 56;
    sub_140833EB0(a1: v60, a2: 1886549113, a3: &v61);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v61 + 16LL))(a1: v61, a2: &v61);
  }
  v44 = qword_141B60C30;
  v45 = 0;
  v46 = nullptr;
  if ( qword_141B60C30 != qword_141B60C38 )
  {
    while ( *(_DWORD *)v44 != 1986359923 )
    {
      v44 += 16;
      if ( v44 == qword_141B60C38 )
        goto LABEL_53;
    }
    if ( v44 == qword_141B60C38 )
      v46 = nullptr;
    else
      v46 = *(__int64 **)(v44 + 8);
  }
LABEL_53:
  v47 = &qword_141B5A4A0;
  if ( v46 != nullptr )
    v47 = v46;
  if ( (*(unsigned __int8 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v47 + 8LL))(a1: *v47, a2: v47) != 0 )
    v45 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v47 + 64LL))(a1: *v47, a2: v47);
  v52 = sub_14083D4F0(a1: v49, a2: v48, a3: v50, a4: v51);
  LODWORD(v62) = v45;
  v61 = v52 + 40;
  sub_140833EB0(a1: v60, a2: 1986359923, a3: &v61);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v61 + 16LL))(a1: v61, a2: &v61);
  v57 = sub_14083D4F0(a1: v54, a2: v53, a3: v55, a4: v56);
  LOBYTE(v62) = 0;
  v61 = v57 + 24;
  sub_140833EB0(a1: v60, a2: 1766410053, a3: &v61);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v61 + 16LL))(a1: v61, a2: &v61);
  sub_140835A40(a1: v60, a2: 1853322860, a3: a4);
  LOBYTE(v58) = 1;
  LOBYTE(v59) = 1;
  v4 = sub_140F47AD0(
         a1: (unsigned int)&qword_141B5FDA8,
         a2: (unsigned int)v60,
         a3: v58,
         a4: v59,
         a5: 1,
         a6: 0,
         a7: 1,
         a8: 0,
         a9: 0,
         a10: 0,
         a11: 0,
         a12: 0);
  sub_140833970(a1: v60);
  return v4;
}
