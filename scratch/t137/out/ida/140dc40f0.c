__int64 __fastcall sub_140DC40F0(__int64 a1, _QWORD *a2, char a3, unsigned int a4)
{
  __int64 v4; // rbp
  __int64 v9; // r12
  _DWORD *v10; // rbx
  __int64 v11; // rax
  __int64 v12; // rsi
  __int64 v13; // rdi
  __int64 v14; // rdi
  __int64 v15; // rbx
  __int64 v16; // rsi
  __int64 v17; // rdx
  _DWORD *v18; // rax
  _DWORD *v19; // rbx
  __int64 *v20; // rax
  __int64 v21; // rbp
  __int64 v22; // rsi
  _DWORD *v23; // rcx
  __int64 v24; // rbx
  __int64 v25; // rbx
  __int64 v26; // rbx
  __int64 v27; // rbx
  __int64 v28; // rbx
  __int64 v29; // rbx
  __int64 v30; // rbx
  __int64 v31; // rbx
  __int64 v32; // rbx
  __int64 v33; // rbx
  __int64 v34; // rbx
  __int64 v35; // rbx
  __int64 v36; // rbx
  __int64 v37; // rbx
  _DWORD *v38; // rbx
  _DWORD *v40; // rbx
  _DWORD *v41; // rbx
  _DWORD *v42; // rbx
  _DWORD *v43; // rbx
  __int64 v44; // rcx
  _DWORD *v45; // rbx
  __int64 v46; // rcx
  __int64 v47; // rbx
  __int64 v48; // rbx
  __int64 v49; // rbx
  __int64 v50; // rbx
  __int64 v51; // rbx
  __int64 v52; // rbx
  __int64 v53; // rbx
  bool v54; // [rsp+29h] [rbp-4Fh] BYREF
  bool v55; // [rsp+2Ah] [rbp-4Eh] BYREF
  char v56; // [rsp+2Bh] [rbp-4Dh] BYREF
  char v57; // [rsp+2Ch] [rbp-4Ch] BYREF
  char v58; // [rsp+2Dh] [rbp-4Bh] BYREF
  char v59; // [rsp+2Eh] [rbp-4Ah] BYREF
  char v60; // [rsp+2Fh] [rbp-49h] BYREF
  char v61; // [rsp+30h] [rbp-48h] BYREF
  char v62; // [rsp+31h] [rbp-47h] BYREF
  char v63; // [rsp+32h] [rbp-46h] BYREF
  char v64; // [rsp+33h] [rbp-45h] BYREF
  __int16 v65; // [rsp+34h] [rbp-44h] BYREF
  _WORD v66[33]; // [rsp+36h] [rbp-42h] BYREF

  v9 = a1 - 248;
  if ( a3 != 0 )
  {
    v10 = (_DWORD *)*a2;
    v11 = *(int *)(*(_QWORD *)(a1 - 240) + 4LL);
    v64 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)(a1 + v11 - 240) + 48LL))(v11 + v9 + 8);
    (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v10 + 40LL))(v10, &v64, 1);
    if ( v10[4] != 0 )
      goto LABEL_48;
    if ( (_BYTE)a4 == 0 )
    {
      LOBYTE(v4) = 1;
      goto LABEL_5;
    }
  }
  else
  {
    LOBYTE(v4) = 1;
    if ( (_BYTE)a4 == 0 )
      return (unsigned int)v4;
  }
  v18 = *(_DWORD **)(a1 - 168);
  v19 = (_DWORD *)*a2;
  if ( v18 != nullptr )
  {
    v66[0] = (unsigned int)(v18[2] - *v18) >> 1;
    (*(void (__fastcall **)(_DWORD *, _WORD *, __int64))(*(_QWORD *)v19 + 40LL))(v19, v66, 2);
    if ( v19[4] != 0 )
      goto LABEL_48;
    v20 = *(__int64 **)(a1 - 168);
    v21 = *v20;
    v22 = v20[1];
    if ( *v20 != v22 )
    {
      v23 = (_DWORD *)*a2;
      do
      {
        (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v23 + 40LL))(v23, 0x14189DFB9LL, 1);
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v21, 2);
        v23 = (_DWORD *)*a2;
        if ( *(_DWORD *)(*a2 + 16LL) != 0 )
          goto LABEL_48;
        v21 += 2;
      }
      while ( v21 != v22 );
    }
  }
  else
  {
    v65 = 0;
    (*(void (__fastcall **)(_DWORD *, __int16 *, __int64))(*(_QWORD *)v19 + 40LL))(v19, &v65, 2);
    if ( v19[4] != 0 )
      goto LABEL_48;
  }
  v24 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 - 40, 2);
  if ( *(_DWORD *)(v24 + 16) != 0 )
    goto LABEL_48;
  v25 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 - 38, 2);
  if ( *(_DWORD *)(v25 + 16) != 0 )
    goto LABEL_48;
  v26 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 - 36, 2);
  if ( *(_DWORD *)(v26 + 16) != 0 )
    goto LABEL_48;
  v27 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 - 34, 2);
  if ( *(_DWORD *)(v27 + 16) != 0 )
    goto LABEL_48;
  v28 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 - 32, 2);
  if ( *(_DWORD *)(v28 + 16) != 0 )
    goto LABEL_48;
  v29 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 - 30, 1);
  if ( *(_DWORD *)(v29 + 16) != 0 )
    goto LABEL_48;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 - 29, 1);
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 - 28, 1);
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 - 27, 1);
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 - 26, 1);
  if ( (unsigned __int8)sub_1413F4E30(a1 - 232, a2) == 0 )
    goto LABEL_48;
  v30 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 - 64, 4);
  if ( *(_DWORD *)(v30 + 16) != 0 )
    goto LABEL_48;
  LODWORD(v4) = 0;
  if ( (unsigned __int8)sub_140F805C0(a2, *(_QWORD *)(a1 - 152), 0) == 0 )
    return (unsigned int)v4;
  LODWORD(v4) = 0;
  if ( (unsigned __int8)sub_140F805C0(a2, *(_QWORD *)(a1 - 144), 0) == 0 )
    return (unsigned int)v4;
  v31 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 - 60, 4);
  if ( *(_DWORD *)(v31 + 16) != 0 )
    goto LABEL_48;
  if ( (unsigned __int8)sub_140DB89D0(a1 - 56, a2) == 0 )
    goto LABEL_48;
  v32 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 - 25, 1);
  if ( *(_DWORD *)(v32 + 16) != 0 )
    goto LABEL_48;
  v33 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 - 24, 1);
  if ( *(_DWORD *)(v33 + 16) != 0 )
    goto LABEL_48;
  v34 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 - 23, 1);
  if ( *(_DWORD *)(v34 + 16) != 0
    || (v35 = *a2,
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 - 22, 1),
        *(_DWORD *)(v35 + 16) != 0)
    || (v36 = *a2,
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 - 21, 1),
        *(_DWORD *)(v36 + 16) != 0)
    || (v37 = *a2,
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 - 20, 1),
        *(_DWORD *)(v37 + 16) != 0)
    || (unsigned __int8)sub_140DB89D0(a1 - 52, a2) == 0
    || (unsigned __int8)sub_140DB89D0(a1 - 48, a2) == 0 )
  {
LABEL_48:
    LODWORD(v4) = 0;
    return (unsigned int)v4;
  }
  v38 = (_DWORD *)*a2;
  if ( *(_QWORD *)(a1 - 72) != 0 )
  {
    v63 = 1;
    (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v38 + 40LL))(v38, &v63, 1);
    if ( v38[4] != 0 || (unsigned __int8)sub_1413F8F10(*(_QWORD *)(a1 - 72), a2) == 0 )
      goto LABEL_48;
  }
  else
  {
    v62 = 0;
    (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v38 + 40LL))(v38, &v62, 1);
    if ( v38[4] != 0 )
      goto LABEL_48;
  }
  v40 = (_DWORD *)*a2;
  if ( *(_QWORD *)(a1 - 128) != 0 )
  {
    v61 = 1;
    (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v40 + 40LL))(v40, &v61, 1);
    if ( v40[4] != 0 || (unsigned __int8)sub_1413FE060(*(_QWORD *)(a1 - 128), a2) == 0 )
      goto LABEL_48;
  }
  else
  {
    v60 = 0;
    (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v40 + 40LL))(v40, &v60, 1);
    if ( v40[4] != 0 )
      goto LABEL_48;
  }
  v41 = (_DWORD *)*a2;
  if ( *(_QWORD *)(a1 - 104) != 0 )
  {
    v59 = 1;
    (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v41 + 40LL))(v41, &v59, 1);
    if ( v41[4] != 0 || (unsigned __int8)sub_1413FE570(*(_QWORD *)(a1 - 104), a2) == 0 )
      goto LABEL_48;
  }
  else
  {
    v58 = 0;
    (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v41 + 40LL))(v41, &v58, 1);
    if ( v41[4] != 0 )
      goto LABEL_48;
  }
  v42 = (_DWORD *)*a2;
  if ( *(_QWORD *)(a1 - 80) != 0 )
  {
    v57 = 1;
    (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v42 + 40LL))(v42, &v57, 1);
    if ( v42[4] == 0 && (unsigned __int8)sub_1413FF050(*(_QWORD *)(a1 - 80), a2) != 0 )
      goto LABEL_67;
    goto LABEL_48;
  }
  v56 = 0;
  (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v42 + 40LL))(v42, &v56, 1);
  if ( v42[4] != 0 )
    goto LABEL_48;
LABEL_67:
  v43 = (_DWORD *)*a2;
  v55 = *(_QWORD *)(a1 - 136) != 0;
  (*(void (__fastcall **)(_DWORD *, bool *, __int64))(*(_QWORD *)v43 + 40LL))(v43, &v55, 1);
  if ( v43[4] != 0 )
    goto LABEL_48;
  v44 = *(_QWORD *)(a1 - 136);
  if ( v44 != 0 && (*(unsigned __int8 (__fastcall **)(__int64, _QWORD *))(*(_QWORD *)v44 + 24LL))(v44, a2) == 0 )
    goto LABEL_48;
  v45 = (_DWORD *)*a2;
  v54 = *(_QWORD *)(a1 - 96) != 0;
  (*(void (__fastcall **)(_DWORD *, bool *, __int64))(*(_QWORD *)v45 + 40LL))(v45, &v54, 1);
  if ( v45[4] != 0 )
    goto LABEL_48;
  v46 = *(_QWORD *)(a1 - 96);
  if ( v46 != 0 && (unsigned __int8)sub_1413FF120(v46, a2) == 0 )
    goto LABEL_48;
  v47 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 - 19, 1);
  if ( *(_DWORD *)(v47 + 16) != 0 )
    goto LABEL_48;
  v48 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 - 18, 1);
  if ( *(_DWORD *)(v48 + 16) != 0 )
    goto LABEL_48;
  v49 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 - 17, 1);
  if ( *(_DWORD *)(v49 + 16) != 0 )
    goto LABEL_48;
  v50 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 - 16, 1);
  if ( *(_DWORD *)(v50 + 16) != 0 )
    goto LABEL_48;
  v51 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 - 15, 1);
  if ( *(_DWORD *)(v51 + 16) != 0 )
    goto LABEL_48;
  v52 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 - 14, 1);
  if ( *(_DWORD *)(v52 + 16) != 0 )
    goto LABEL_48;
  v53 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 - 13, 1);
  LOBYTE(v4) = *(_DWORD *)(v53 + 16) == 0;
  if ( *(_DWORD *)(v53 + 16) != 0 )
    return (unsigned int)v4;
LABEL_5:
  if ( a3 != 0 )
  {
    LODWORD(v4) = 0;
    if ( (unsigned __int8)sub_140DDADF0(*(int *)(*(_QWORD *)(a1 - 240) + 8LL) + v9 + 344, a2, 0, a4) != 0 )
    {
      LODWORD(v4) = 0;
      if ( (unsigned __int8)sub_140DFC460(*(int *)(*(_QWORD *)(a1 - 240) + 8LL) + v9 + 128, a2, 0, a4) != 0 )
      {
        v12 = *(int *)(*(_QWORD *)(a1 - 240) + 4LL);
        v13 = *a2;
        (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v12 + v9 + 32, 8);
        if ( *(_DWORD *)(v13 + 16) == 0 )
        {
          v14 = v12 + v9 + 8;
          v15 = *a2;
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v12 + v9 + 16, 4);
          if ( *(_DWORD *)(v15 + 16) == 0 )
          {
            v4 = *a2;
            (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v12 + v9 + 20, 4);
            if ( *(_DWORD *)(v4 + 16) == 0 )
            {
              v16 = *a2;
              v17 = *(_DWORD *)(v14 + 16) != 0 ? v14 + 16 : v14 + 12;
              (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v17, 4);
              if ( *(_DWORD *)(v16 + 16) == 0 )
              {
                LOBYTE(v4) = 1;
                return (unsigned int)v4;
              }
            }
          }
        }
        goto LABEL_48;
      }
    }
  }
  return (unsigned int)v4;
}
