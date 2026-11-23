__int64 __fastcall sub_140E089C0(__int64 a1, volatile signed __int32 **a2, char a3, unsigned int a4)
{
  volatile signed __int32 *v4; // rsi
  char v6; // bl
  volatile signed __int32 **v7; // rdi
  volatile signed __int32 *v9; // rax
  _QWORD *v10; // r12
  __int64 v11; // r13
  volatile signed __int32 *v12; // rsi
  __int64 v13; // rax
  int v14; // eax
  __int64 v15; // rsi
  int v16; // eax
  __int64 v17; // rcx
  __int64 v18; // rax
  _QWORD *v19; // rdx
  __int64 v20; // r8
  volatile signed __int32 *v21; // rsi
  _QWORD *v22; // rsi
  __int64 v23; // r8
  bool v24; // zf
  volatile signed __int32 *v25; // rsi
  volatile signed __int32 *v26; // rsi
  volatile signed __int32 *v27; // rsi
  volatile signed __int32 *v28; // rsi
  _QWORD *v29; // rdi
  __int64 v30; // r8
  __int64 v31; // rax
  __int64 v32; // r15
  char *v33; // rax
  __int64 v34; // rsi
  __int64 v35; // r8
  char *v36; // rbx
  __int64 v37; // rcx
  __int64 v38; // rbx
  char *v39; // rbx
  __int64 v40; // rsi
  __int64 v41; // r8
  __int64 v42; // r8
  volatile signed __int32 *v43; // rsi
  volatile signed __int32 *v44; // rcx
  __int64 v45; // rsi
  volatile signed __int32 *v46; // rbx
  volatile signed __int32 *v47; // rsi
  __int64 v48; // rsi
  __int64 v49; // rsi
  volatile signed __int32 *v50; // rsi
  __int64 v51; // rsi
  __int64 v52; // rcx
  volatile signed __int32 *v53; // rsi
  __int64 v54; // rsi
  __int64 v55; // r12
  volatile signed __int32 *v56; // rbx
  char v57; // al
  volatile signed __int32 *v58; // rsi
  __int64 v59; // rcx
  volatile signed __int32 *v60; // rsi
  __int64 v61; // rax
  int v62; // eax
  volatile signed __int32 *v63; // rsi
  __int64 v64; // rax
  int v65; // eax
  volatile signed __int32 *v66; // rsi
  __int64 v67; // r8
  __int64 v68; // r15
  __int64 v69; // r14
  volatile signed __int32 *v70; // rsi
  volatile signed __int32 *v71; // rbx
  volatile signed __int32 *v72; // rbx
  volatile signed __int32 *v73; // rbx
  volatile signed __int32 *v74; // rcx
  __int64 v75; // rdx
  char *v77; // [rsp+48h] [rbp-38h]
  volatile signed __int32 **v78; // [rsp+50h] [rbp-30h]
  int v79; // [rsp+58h] [rbp-28h] BYREF
  unsigned __int8 v80; // [rsp+5Eh] [rbp-22h]
  char v81; // [rsp+5Fh] [rbp-21h]
  __int64 v82; // [rsp+60h] [rbp-20h] BYREF
  unsigned __int8 v83; // [rsp+6Fh] [rbp-11h] BYREF
  volatile signed __int32 *v84; // [rsp+70h] [rbp-10h] BYREF
  _QWORD *v85; // [rsp+78h] [rbp-8h]
  __int64 v86; // [rsp+80h] [rbp+0h]
  char *v87; // [rsp+88h] [rbp+8h]
  __int64 v88; // [rsp+90h] [rbp+10h]

  v88 = -2;
  v6 = a3;
  v7 = a2;
  if ( a3 != 0 )
  {
    v4 = *a2;
    LOBYTE(v84) = 2;
    (*(void (__fastcall **)(volatile signed __int32 *, volatile signed __int32 **, __int64))(*(_QWORD *)v4 + 40LL))(
      a1: v4,
      a2: &v84,
      a3: 1);
    if ( *((_DWORD *)v4 + 4) != 0 )
      goto LABEL_198;
  }
  if ( (_BYTE)a4 == 0 )
    goto LABEL_188;
  v81 = v6;
  v9 = *v7;
  v84 = v9;
  if ( v9 != nullptr )
    _InterlockedIncrement(v9 + 2);
  v85 = (_QWORD *)(a1 - 126);
  v86 = 10;
  v87 = (char *)(a1 - 116);
  v78 = v7;
  v80 = a4;
  if ( v84 != nullptr )
  {
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v84 + 40LL))(
      a1: v84,
      a2: a1 - 126,
      a3: 10);
    v85 = (_QWORD *)(a1 - 19);
    v86 = 1;
    v10 = (_QWORD *)(a1 - 18);
    v87 = (char *)(a1 - 18);
    if ( v84 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v84 + 40LL))(
        a1: v84,
        a2: a1 - 19,
        a3: 1);
  }
  else
  {
    v10 = (_QWORD *)(a1 - 18);
  }
  v85 = (_QWORD *)(a1 - 23);
  v86 = 4;
  v87 = (char *)(a1 - 19);
  if ( v84 == nullptr )
  {
    v11 = a1 - 16;
    goto LABEL_14;
  }
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v84 + 40LL))(
    a1: v84,
    a2: a1 - 23,
    a3: 4);
  v85 = v10;
  v86 = 2;
  v11 = a1 - 16;
  v87 = (char *)(a1 - 16);
  if ( v84 == nullptr )
  {
LABEL_14:
    v12 = nullptr;
    goto LABEL_15;
  }
  (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v84 + 40LL))(
    a1: v84,
    a2: v10,
    a3: 2);
  v12 = v84;
LABEL_15:
  v87 = nullptr;
  v86 = 0;
  v85 = nullptr;
  v13 = *(_QWORD *)(a1 - 336);
  if ( v13 != 0 )
    v14 = *(_DWORD *)(v13 + 8);
  else
    v14 = -1;
  LODWORD(v82) = v14;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64 *, __int64))(*(_QWORD *)v12 + 40LL))(
    a1: v12,
    a2: &v82,
    a3: 4);
  if ( *((_DWORD *)v12 + 4) != 0 )
    goto LABEL_97;
  v15 = *(_QWORD *)(a1 - 328);
  if ( v86 != 0 && v84 != nullptr )
    (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *))(*(_QWORD *)v84 + 40LL))(a1: v84, a2: v85);
  v87 = nullptr;
  v86 = 0;
  v85 = nullptr;
  if ( v15 != 0 )
  {
    v16 = *(_DWORD *)(v15 + 8);
    v17 = v16;
  }
  else
  {
    v16 = -1;
    v17 = -1;
  }
  v82 = v17;
  if ( BYTE5(qword_141B6034C) == 0 || byte_141B5FC2C != 0 )
  {
    v79 = v16;
    v18 = *(_QWORD *)v84;
    v19 = &v79;
    v20 = 4;
  }
  else
  {
    v18 = *(_QWORD *)v84;
    v19 = &v82;
    v20 = 8;
  }
  (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(v18 + 40))(a1: v84, a2: v19, a3: v20);
  if ( v86 != 0 && v84 != nullptr )
    (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *))(*(_QWORD *)v84 + 40LL))(a1: v84, a2: v85);
  v87 = nullptr;
  v86 = 0;
  v85 = nullptr;
  v21 = v84;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v84 + 40LL))(
    a1: v84,
    a2: a1 - 112,
    a3: 69);
  if ( *((_DWORD *)v21 + 4) != 0 )
  {
LABEL_97:
    if ( v86 != 0 )
    {
      if ( v84 == nullptr )
      {
LABEL_198:
        LODWORD(v4) = 0;
        return (unsigned int)v4;
      }
      (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *))(*(_QWORD *)v84 + 40LL))(a1: v84, a2: v85);
    }
    v44 = v84;
    v87 = nullptr;
    v86 = 0;
    v85 = nullptr;
    if ( v84 != nullptr && _InterlockedDecrement(v84 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v44)(a1: v44, a2: 1);
    goto LABEL_198;
  }
  if ( v87 == (char *)(a1 - 168) )
  {
    v22 = (_QWORD *)(a1 - 25);
    v24 = v86 == -4;
    v23 = v86 + 4;
    v86 += 4;
    v77 = (char *)(a1 - 164);
    v87 = (char *)(a1 - 164);
    if ( v24 )
      goto LABEL_41;
  }
  else
  {
    if ( v86 != 0 && v84 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v84 + 40LL))(
        a1: v84,
        a2: v85,
        a3: v86);
    v85 = (_QWORD *)(a1 - 168);
    v86 = 4;
    v77 = (char *)(a1 - 164);
    v87 = (char *)(a1 - 164);
    v22 = (_QWORD *)(a1 - 25);
    v23 = 4;
  }
  if ( v84 != nullptr )
    (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v84 + 40LL))(
      a1: v84,
      a2: v85,
      a3: v23);
LABEL_41:
  v85 = v22;
  v86 = 1;
  v87 = (char *)(a1 - 24);
  if ( v84 != nullptr )
    (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v84 + 40LL))(
      a1: v84,
      a2: v22,
      a3: 1);
  v85 = (_QWORD *)(a1 - 140);
  v86 = 14;
  v87 = (char *)(a1 - 126);
  if ( v84 != nullptr )
  {
    (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v84 + 40LL))(
      a1: v84,
      a2: v85,
      a3: 14);
    v85 = (_QWORD *)(a1 - 116);
    v86 = 4;
    v87 = (char *)(a1 - 112);
    if ( v84 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v84 + 40LL))(
        a1: v84,
        a2: a1 - 116,
        a3: 4);
  }
  v85 = (_QWORD *)(a1 - 29);
  v86 = 4;
  v87 = (char *)v22;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v84 + 40LL))(
    a1: v84,
    a2: a1 - 29,
    a3: 4);
  v25 = v84;
  v85 = nullptr;
  v86 = 0;
  v87 = nullptr;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v84 + 40LL))(
    a1: v84,
    a2: 0x1418B72F4LL,
    a3: 1);
  if ( *((_DWORD *)v25 + 4) != 0 )
    goto LABEL_97;
  v26 = v84;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v84 + 40LL))(
    a1: v84,
    a2: a1 - 300,
    a3: 2);
  if ( *((_DWORD *)v26 + 4) != 0 )
    goto LABEL_97;
  v27 = v84;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v84 + 40LL))(
    a1: v84,
    a2: a1 - 298,
    a3: 2);
  if ( *((_DWORD *)v27 + 4) != 0 )
    goto LABEL_97;
  v28 = v84;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v84 + 40LL))(
    a1: v84,
    a2: a1 - 304,
    a3: 4);
  if ( *((_DWORD *)v28 + 4) != 0 )
    goto LABEL_97;
  if ( v87 == (char *)(a1 - 144) )
  {
    v24 = v86 == -4;
    v30 = v86 + 4;
    v86 += 4;
    v87 = (char *)(a1 - 140);
    v29 = (_QWORD *)(a1 - 24);
    if ( v24 )
      goto LABEL_58;
  }
  else
  {
    v29 = (_QWORD *)(a1 - 24);
    if ( v86 != 0 && v84 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v84 + 40LL))(
        a1: v84,
        a2: v85,
        a3: v86);
    v85 = (_QWORD *)(a1 - 144);
    v86 = 4;
    v87 = (char *)(a1 - 140);
    v30 = 4;
  }
  if ( v84 != nullptr )
    (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v84 + 40LL))(
      a1: v84,
      a2: v85,
      a3: v30);
LABEL_58:
  v85 = v29;
  v86 = 1;
  v87 = (char *)(a1 - 23);
  LODWORD(v82) = *(unsigned __int8 *)(a1 - 43);
  if ( (__int64 *)(a1 - 23) == &v82 )
  {
    v31 = 5;
  }
  else
  {
    if ( v84 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v84 + 40LL))(
        a1: v84,
        a2: v29,
        a3: 1);
    v85 = &v82;
    v31 = 4;
  }
  v86 = v31;
  v87 = (char *)&v82 + 4;
  sub_1412E70A0(a1: &v84);
  v32 = *(unsigned __int8 *)(a1 - 43);
  if ( *(_BYTE *)(a1 - 43) != 0 )
  {
    v33 = v87;
    v34 = 0;
    do
    {
      v37 = *(unsigned __int8 *)(a1 - 30);
      v38 = v34 + v37 - 12;
      if ( (unsigned __int64)(v34 + v37) < 0xC )
        v38 = v34 + v37;
      v39 = (char *)(a1 - 42 + v38);
      if ( v33 == v39 )
      {
        v35 = v86 + 1;
      }
      else
      {
        if ( v86 != 0 && v84 != nullptr )
          (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v84 + 40LL))(
            a1: v84,
            a2: v85,
            a3: v86);
        v85 = v39;
        v35 = 1;
      }
      v86 = v35;
      v36 = v39 + 1;
      v87 = v36;
      ++v34;
      v33 = v36;
    }
    while ( v32 != v34 );
  }
  else
  {
    v36 = v87;
  }
  if ( v36 == v77 )
  {
    v40 = a1 - 264;
    v24 = v86 == -4;
    v41 = v86 + 4;
    v86 += 4;
    v87 = (char *)(a1 - 160);
    if ( v24 )
      goto LABEL_83;
  }
  else
  {
    if ( v86 != 0 && v84 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v84 + 40LL))(
        a1: v84,
        a2: v85,
        a3: v86);
    v85 = v77;
    v86 = 4;
    v87 = (char *)(a1 - 160);
    v40 = a1 - 264;
    v41 = 4;
  }
  if ( v84 != nullptr )
    (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v84 + 40LL))(
      a1: v84,
      a2: v85,
      a3: v41);
LABEL_83:
  v87 = nullptr;
  v86 = 0;
  v85 = nullptr;
  if ( (unsigned __int8)sub_141460430(a1: v40, a2: &v84) == 0 )
    goto LABEL_97;
  if ( v86 != 0 && v84 != nullptr )
    (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *))(*(_QWORD *)v84 + 40LL))(a1: v84, a2: v85);
  v87 = nullptr;
  v86 = 0;
  v85 = nullptr;
  sub_1408149D0(a1: v84, a2: &v82, a3: a1 - 392);
  if ( (_DWORD)v82 != 0 )
    goto LABEL_97;
  if ( v87 == (char *)(a1 - 156) )
  {
    v24 = v86 == -12;
    v42 = v86 + 12;
    v86 += 12;
    v87 = (char *)(a1 - 144);
    if ( v24 )
      goto LABEL_96;
  }
  else
  {
    if ( v86 != 0 && v84 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v84 + 40LL))(
        a1: v84,
        a2: v85,
        a3: v86);
    v85 = (_QWORD *)(a1 - 156);
    v86 = 12;
    v87 = (char *)(a1 - 144);
    v42 = 12;
  }
  if ( v84 != nullptr )
    (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v84 + 40LL))(
      a1: v84,
      a2: v85,
      a3: v42);
LABEL_96:
  v87 = nullptr;
  v86 = 0;
  v85 = nullptr;
  v43 = v84;
  LOBYTE(v82) = *(_QWORD *)(a1 - 360) != 0;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64 *, __int64))(*(_QWORD *)v84 + 40LL))(
    a1: v84,
    a2: &v82,
    a3: 1);
  if ( *((_DWORD *)v43 + 4) != 0 )
    goto LABEL_97;
  v45 = *(_QWORD *)(a1 - 360);
  if ( v45 != 0 )
  {
    if ( v86 != 0 && v84 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *))(*(_QWORD *)v84 + 40LL))(a1: v84, a2: v85);
    v87 = nullptr;
    v86 = 0;
    v85 = nullptr;
    v46 = v84;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v84 + 40LL))(
      a1: v84,
      a2: v45,
      a3: 30);
    if ( *((_DWORD *)v46 + 4) != 0 )
      goto LABEL_97;
  }
  if ( v86 != 0 && v84 != nullptr )
    (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *))(*(_QWORD *)v84 + 40LL))(a1: v84, a2: v85);
  v87 = nullptr;
  v86 = 0;
  v85 = nullptr;
  v47 = v84;
  LOBYTE(v82) = *(_QWORD *)(a1 - 384) != 0;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64 *, __int64))(*(_QWORD *)v84 + 40LL))(
    a1: v84,
    a2: &v82,
    a3: 1);
  if ( *((_DWORD *)v47 + 4) != 0 )
    goto LABEL_97;
  v48 = *(_QWORD *)(a1 - 384);
  if ( v48 != 0 )
  {
    if ( v86 != 0 && v84 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *))(*(_QWORD *)v84 + 40LL))(a1: v84, a2: v85);
    v87 = nullptr;
    v86 = 0;
    v85 = nullptr;
    if ( (unsigned __int8)sub_14146C2A0(a1: v48, a2: &v84) == 0 )
      goto LABEL_97;
  }
  v49 = *(_QWORD *)(a1 - 400);
  LOBYTE(v79) = v49 != 0;
  if ( v87 == (char *)&v79 )
  {
    ++v86;
  }
  else
  {
    if ( v86 != 0 && v84 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v84 + 40LL))(
        a1: v84,
        a2: v85,
        a3: v86);
    v85 = &v79;
    v86 = 1;
    v49 = *(_QWORD *)(a1 - 400);
  }
  v87 = (char *)&v79 + 1;
  if ( v49 != 0 )
  {
    if ( v86 != 0 && v84 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *))(*(_QWORD *)v84 + 40LL))(a1: v84, a2: v85);
    v87 = nullptr;
    v86 = 0;
    v85 = nullptr;
    if ( (unsigned __int8)sub_14144B040(a1: v49, a2: &v84) == 0 )
      goto LABEL_143;
  }
  if ( v86 != 0 && v84 != nullptr )
    (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *))(*(_QWORD *)v84 + 40LL))(a1: v84, a2: v85);
  v87 = nullptr;
  v86 = 0;
  v85 = nullptr;
  v50 = v84;
  LOBYTE(v82) = *(_QWORD *)(a1 - 344) != 0;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64 *, __int64))(*(_QWORD *)v84 + 40LL))(
    a1: v84,
    a2: &v82,
    a3: 1);
  if ( *((_DWORD *)v50 + 4) != 0 )
    goto LABEL_143;
  v51 = *(_QWORD *)(a1 - 344);
  if ( v51 != 0 )
  {
    if ( v86 != 0 && v84 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *))(*(_QWORD *)v84 + 40LL))(a1: v84, a2: v85);
    v87 = nullptr;
    v86 = 0;
    v85 = nullptr;
    if ( (unsigned __int8)sub_14146E1B0(a1: v51, a2: &v84) == 0 )
      goto LABEL_143;
  }
  LOBYTE(v52) = 100;
  if ( (unsigned __int64)((__int64)(*(_QWORD *)(a1 - 608) - *(_QWORD *)(a1 - 616)) >> 3) < 0x64 )
    v52 = (__int64)(*(_QWORD *)(a1 - 608) - *(_QWORD *)(a1 - 616)) >> 3;
  v83 = v52;
  if ( v86 != 0 && v84 != nullptr )
    (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *))(*(_QWORD *)v84 + 40LL))(a1: v84, a2: v85);
  v87 = nullptr;
  v86 = 0;
  v85 = nullptr;
  v53 = v84;
  (*(void (__fastcall **)(volatile signed __int32 *, unsigned __int8 *, __int64))(*(_QWORD *)v84 + 40LL))(
    a1: v84,
    a2: &v83,
    a3: 1);
  if ( *((_DWORD *)v53 + 4) != 0 )
    goto LABEL_143;
  if ( v83 != 0 )
  {
    v54 = 0;
    do
    {
      v55 = *(_QWORD *)(*(_QWORD *)(a1 - 616) + 8 * v54);
      v56 = *v78;
      v57 = v55 != 0
          ? (*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)v55 + 32LL))(a1: *(_QWORD *)(*(_QWORD *)(a1 - 616) + 8 * v54))
          : -1;
      LOBYTE(v82) = v57;
      (*(void (__fastcall **)(volatile signed __int32 *, __int64 *, __int64))(*(_QWORD *)v56 + 40LL))(
        a1: v56,
        a2: &v82,
        a3: 1);
      if ( *((_DWORD *)v56 + 4) != 0 )
        goto LABEL_143;
      if ( v55 != 0 )
      {
        if ( v86 != 0 && v84 != nullptr )
          (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *))(*(_QWORD *)v84 + 40LL))(a1: v84, a2: v85);
        v87 = nullptr;
        v86 = 0;
        v85 = nullptr;
        if ( (*(unsigned __int8 (__fastcall **)(__int64, volatile signed __int32 **))(*(_QWORD *)v55 + 16LL))(
               a1: v55,
               a2: &v84) == 0 )
          goto LABEL_143;
      }
    }
    while ( ++v54 < (unsigned __int64)v83 );
  }
  if ( v86 != 0 && v84 != nullptr )
    (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *))(*(_QWORD *)v84 + 40LL))(a1: v84, a2: v85);
  v87 = nullptr;
  v86 = 0;
  v85 = nullptr;
  v58 = v84;
  LOBYTE(v82) = *(_QWORD *)(a1 - 376) != 0;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64 *, __int64))(*(_QWORD *)v84 + 40LL))(
    a1: v84,
    a2: &v82,
    a3: 1);
  if ( *((_DWORD *)v58 + 4) != 0 )
    goto LABEL_143;
  v59 = *(_QWORD *)(a1 - 376);
  if ( v59 != 0 )
    sub_140E06000(a1: v59, a2: v78);
  if ( v86 != 0 && v84 != nullptr )
    (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *))(*(_QWORD *)v84 + 40LL))(a1: v84, a2: v85);
  v87 = nullptr;
  v86 = 0;
  v85 = nullptr;
  v60 = v84;
  v61 = *(_QWORD *)(a1 - 320);
  v62 = v61 != 0 ? *(_DWORD *)(v61 + 8) : -1;
  LODWORD(v82) = v62;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64 *, __int64))(*(_QWORD *)v84 + 40LL))(
    a1: v84,
    a2: &v82,
    a3: 4);
  if ( *((_DWORD *)v60 + 4) != 0 )
    goto LABEL_143;
  if ( v86 != 0 && v84 != nullptr )
    (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *))(*(_QWORD *)v84 + 40LL))(a1: v84, a2: v85);
  v87 = nullptr;
  v86 = 0;
  v85 = nullptr;
  v63 = v84;
  v64 = *(_QWORD *)(a1 - 312);
  v65 = v64 != 0 ? *(_DWORD *)(v64 + 8) : -1;
  LODWORD(v82) = v65;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64 *, __int64))(*(_QWORD *)v84 + 40LL))(
    a1: v84,
    a2: &v82,
    a3: 4);
  if ( *((_DWORD *)v63 + 4) != 0 || (unsigned __int8)sub_14145D6C0(a1: a1 - 296, a2: v78) == 0 )
    goto LABEL_143;
  if ( v86 != 0 && v84 != nullptr )
    (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *))(*(_QWORD *)v84 + 40LL))(a1: v84, a2: v85);
  v87 = nullptr;
  v86 = 0;
  v85 = nullptr;
  v66 = v84;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v84 + 40LL))(a1: v84, a2: v11, a3: 1);
  if ( *((_DWORD *)v66 + 4) != 0 )
  {
LABEL_143:
    sub_1412E6FF0(a1: &v84);
    goto LABEL_198;
  }
  LODWORD(v4) = a1 - 15;
  if ( v87 == (char *)(a1 - 15) )
  {
    v67 = v86 + 3;
  }
  else
  {
    if ( v86 != 0 && v84 != nullptr )
      (*(void (__fastcall **)(volatile signed __int32 *, _QWORD *, __int64))(*(_QWORD *)v84 + 40LL))(
        a1: v84,
        a2: v85,
        a3: v86);
    v85 = (_QWORD *)(a1 - 15);
    v67 = 3;
  }
  v86 = v67;
  v87 = (char *)(a1 - 12);
  sub_1412E6FF0(a1: &v84);
  v7 = v78;
  a4 = v80;
  v6 = v81;
LABEL_188:
  LOBYTE(v4) = 1;
  if ( v6 != 0 )
  {
    v68 = a1 - 632;
    LODWORD(v4) = 0;
    if ( (unsigned __int8)sub_140DDADF0(a1: *(int *)(*(_QWORD *)(a1 - 624) + 8LL) + a1 - 632 + 344, a2: v7, a3: 0, a4) != 0 )
    {
      LODWORD(v4) = 0;
      if ( (unsigned __int8)sub_140DFC460(a1: *(int *)(*(_QWORD *)(a1 - 624) + 8LL) + v68 + 128, a2: v7, a3: 0, a4) != 0 )
      {
        v69 = *(int *)(*(_QWORD *)(a1 - 624) + 4LL);
        v70 = *v7;
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*v7 + 40LL))(
          a1: *v7,
          a2: v69 + v68 + 32,
          a3: 8);
        if ( *((_DWORD *)v70 + 4) != 0 )
          goto LABEL_198;
        LODWORD(v4) = v69 + v68 + 8;
        v71 = *v7;
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*v7 + 40LL))(
          a1: *v7,
          a2: v69 + v68 + 16,
          a3: 4);
        if ( *((_DWORD *)v71 + 4) != 0 )
          goto LABEL_198;
        v72 = *v7;
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*v7 + 40LL))(
          a1: *v7,
          a2: v69 + v68 + 20,
          a3: 4);
        if ( *((_DWORD *)v72 + 4) != 0 )
          goto LABEL_198;
        v73 = *v7;
        if ( *(_DWORD *)(v69 + v68 + 24) != 0 )
        {
          LODWORD(v4) = v69 + v68 + 24;
          v74 = *v7;
          v75 = v69 + v68 + 24;
        }
        else
        {
          v74 = *v7;
          v75 = v69 + v68 + 20;
        }
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*v7 + 40LL))(
          a1: v74,
          a2: v75,
          a3: 4);
        LOBYTE(v4) = 1;
        if ( *((_DWORD *)v73 + 4) != 0 )
          goto LABEL_198;
      }
    }
  }
  return (unsigned int)v4;
}
