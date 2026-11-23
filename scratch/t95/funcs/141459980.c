char __fastcall sub_141459980(__int64 a1, int a2, __int64 *a3)
{
  __int64 *v3; // r15
  int v5; // esi
  __int64 v6; // rax
  unsigned __int64 v7; // rax
  __int64 v8; // rcx
  __int64 *v9; // r12
  __int64 v10; // rax
  __int64 v11; // rcx
  unsigned __int64 v12; // rax
  __int64 v13; // rcx
  __int64 v14; // rcx
  int v15; // eax
  int v16; // ecx
  __int64 v17; // rcx
  int v18; // eax
  int v19; // ecx
  __int64 v20; // rcx
  __int64 v21; // rsi
  __int64 v22; // rdx
  __int64 v23; // r13
  __int64 v24; // rbx
  __int64 v25; // rbx
  __int64 v26; // rax
  __int64 v27; // rcx
  __int64 v28; // rdi
  unsigned __int64 v29; // rbx
  __int64 v30; // rsi
  __int64 v31; // rax
  __int64 v32; // rax
  __int64 v33; // rcx
  __int64 v34; // rdx
  unsigned __int64 v35; // rdi
  unsigned __int64 v36; // r13
  __int64 v37; // rsi
  __int64 v38; // r15
  unsigned __int64 v39; // rcx
  __int64 v40; // r8
  __int64 v41; // r14
  bool v42; // al
  __int64 v44; // rcx
  __int64 v45; // rax
  __int64 v46; // rcx
  __int64 v47; // rax
  __int64 v48; // rcx
  __int64 v49; // rdx
  unsigned __int64 v50; // rsi
  unsigned __int64 v51; // r15
  __int64 v52; // r12
  __int64 v53; // r14
  unsigned __int64 v54; // rcx
  __int64 v55; // r8
  __int64 v56; // rcx
  unsigned __int64 v57; // rdi
  bool v58; // al
  __int64 v59; // rsi
  __int64 v60; // rbx
  __int64 v61; // rax
  __int64 v62; // rdi
  __int64 v63; // rsi
  __int64 v64; // r15
  __int64 v65; // rax
  int v66; // ecx
  __int64 *v67; // rdi
  __int64 v68; // rcx
  __int64 v69; // rax
  __int64 v70; // rcx
  unsigned __int64 v71; // rbx
  __int64 v72; // rcx
  __int64 v73; // rsi
  bool v74; // al
  unsigned __int64 v75; // rcx
  __int64 v76; // rbx
  __int64 v77; // rsi
  bool v78; // al
  _DWORD v79[2]; // [rsp+20h] [rbp-60h] BYREF
  __int64 v80; // [rsp+28h] [rbp-58h]
  __int64 v81; // [rsp+30h] [rbp-50h]
  __int64 *v82; // [rsp+38h] [rbp-48h]
  __int64 v83; // [rsp+40h] [rbp-40h] BYREF
  __int64 v84; // [rsp+48h] [rbp-38h]
  __int64 v85; // [rsp+50h] [rbp-30h] BYREF
  __int64 v86; // [rsp+58h] [rbp-28h]
  __int64 v87; // [rsp+60h] [rbp-20h]
  unsigned __int64 v88; // [rsp+68h] [rbp-18h] BYREF
  __int64 v89; // [rsp+70h] [rbp-10h] BYREF
  unsigned __int64 v90; // [rsp+78h] [rbp-8h]
  __int64 v91; // [rsp+80h] [rbp+0h]

  v91 = -2;
  v3 = a3;
  if ( a2 <= 1282302323 )
  {
    if ( a2 != 1281583476 )
    {
      if ( a2 != 1282172787 )
      {
        if ( a2 == 1282302317 )
        {
          v9 = (__int64 *)(a1 + 24);
          v10 = sub_14083D4F0(a1);
          v89 = 0;
          if ( &v89 != v9 )
          {
            v11 = *v9;
            if ( *v9 != 0 )
              _InterlockedIncrement((volatile signed __int32 *)(v11 - 4));
            v89 = v11;
          }
          v6 = v10 + 136;
          v88 = v6;
          if ( &v88 != (unsigned __int64 *)v3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v3 + 16LL))(*v3, v3);
            v12 = v88;
            v13 = v89;
            v3[1] = v89;
            *v3 = v12;
            v6 = sub_14083D4F0(v13) + 8;
            v89 = 0;
            v88 = v6;
          }
          goto LABEL_7;
        }
        return sub_140FE3F20((_DWORD *)a1, a2, a3);
      }
      sub_1407C9510(&v88);
      v26 = *(_QWORD *)(a1 + 48);
      v27 = *(_QWORD *)(a1 + 56);
      if ( v27 != v26 )
      {
        v28 = 0;
        v29 = 0;
        do
        {
          v30 = *(_QWORD *)(v26 + v28);
          if ( v30 != 0 )
          {
            v31 = sub_14083D4F0(v27);
            v86 = 0;
            v85 = v31 + 8;
            sub_140F10C50(v30, &v85);
            sub_14083B2B0(&v88, &v85);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v85 + 16LL))(v85, &v85);
            v26 = *(_QWORD *)(a1 + 48);
            v27 = *(_QWORD *)(a1 + 56);
          }
          ++v29;
          v28 += 16;
        }
        while ( v29 < (v27 - v26) >> 4 );
      }
      sub_14083DB80(&v85, &v88);
      v44 = *v3;
      if ( &v85 != v3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v44 + 16LL))(v44, v3);
        v45 = v85;
        v46 = v86;
        v3[1] = v86;
        *v3 = v45;
        v44 = sub_14083D4F0(v46) + 8;
        v86 = 0;
        v85 = v44;
      }
LABEL_53:
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v44 + 16LL))(v44, &v85);
      sub_14083B0A0(&v88);
      return 1;
    }
    sub_141729A10(&v85, a1);
    v21 = v86 - v85;
    v22 = v86 - v85;
    v82 = v3;
    if ( v86 == v85 )
    {
      v25 = 0;
      v80 = 0;
      v23 = 0;
    }
    else
    {
      if ( v86 - v85 < 0 )
        sub_1400526C0(v20, v22);
      v23 = sub_1407E4490(qword_141ABD470, v22);
      v80 = v23 + 8 * (v21 >> 3);
      v24 = v86 - v85;
      sub_141758A00(v23, v85, v86 - v85);
      v25 = v23 + v24;
    }
    sub_1407C9510(&v88);
    v34 = v25 - v23;
    v50 = (v25 - v23) >> 3;
    v51 = v88;
    if ( (__int64)(v90 - v88) >> 3 < v50 )
    {
      if ( v34 < 0 )
        goto LABEL_124;
      v52 = v89;
      v53 = sub_1407E4490(qword_141ABD470, v34);
      sub_141758A00(v53, v88, v89 - v88);
      if ( v88 != 0 )
      {
        v54 = v90 - v88;
        if ( v90 - v88 == -1 )
          v54 = *(unsigned int *)(v88 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v55 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v55) >> 3 > v54)
          && (v56 = *(_QWORD *)(v55 + 8 * v54)) != 0 )
        {
          v57 = v88 - *(unsigned int *)(v56 + 120);
          v81 = v56;
          MEMORY[0x1419475D8](v56 + 32, v57);
          v33 = v81;
          v58 = *(_BYTE *)(v81 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v81 + 64)) != 0;
          if ( !v58 && *(_BYTE *)(v81 + 97) != 0 )
            sub_1412D33C0(v81);
        }
        else
        {
          MEMORY[0x141948990](v88 - *(unsigned int *)(qword_141ABD470 + 48));
        }
      }
      v88 = v53;
      v89 = v53 + v52 - v51;
      v90 = v53 + 8 * v50;
    }
    if ( v25 != v23 )
    {
      v62 = 1;
      if ( v50 >= 2 )
        v62 = (v25 - v23) >> 3;
      v63 = 0;
      do
      {
        v64 = *(_QWORD *)(v23 + 8 * v63);
        if ( v64 != 0 )
        {
          v65 = sub_14083D4F0(v33);
          v84 = 0;
          v83 = v65 + 8;
          v66 = *(_DWORD *)(v64 + 16);
          if ( v66 == 0 )
            v66 = *(_DWORD *)(v64 + 12);
          v79[0] = *(_DWORD *)(v64 + 12);
          v79[1] = v66;
          sub_140FE72B0(v79, 1667855481, &v83);
          sub_14083B5F0(&v88, &v83);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v83 + 16LL))(v83, &v83);
        }
        ++v63;
      }
      while ( v62 != v63 );
    }
    sub_14083DB80(&v83, &v88);
    v67 = v82;
    v68 = *v82;
    if ( &v83 != v82 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v68 + 16LL))(v68, v82);
      v69 = v83;
      v70 = v84;
      v67[1] = v84;
      *v67 = v69;
      v68 = sub_14083D4F0(v70) + 8;
      v84 = 0;
      v83 = v68;
    }
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v68 + 16LL))(v68, &v83);
    sub_14083B0A0(&v88);
    if ( v23 != 0 )
    {
      v71 = v80 - v23;
      if ( v80 - v23 == -1 )
        v71 = *(unsigned int *)(v23 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
        && (v72 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v72) >> 3 > v71)
        && (v73 = *(_QWORD *)(v72 + 8 * v71)) != 0 )
      {
        MEMORY[0x1419475D8](v73 + 32, v23 - *(unsigned int *)(v73 + 120));
        v74 = *(_BYTE *)(v73 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v73 + 64)) != 0;
        if ( !v74 && *(_BYTE *)(v73 + 97) != 0 )
          sub_1412D33C0(v73);
      }
      else
      {
        MEMORY[0x141948990](v23 - *(unsigned int *)(qword_141ABD470 + 48));
      }
    }
    if ( v85 != 0 )
    {
      v75 = v87 - v85;
      if ( v87 - v85 == -1 )
        v75 = *(unsigned int *)(v85 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
        && (v76 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v76) >> 3 > v75)
        && (v77 = *(_QWORD *)(v76 + 8 * v75)) != 0 )
      {
        MEMORY[0x1419475D8](v77 + 32, v85 - *(unsigned int *)(v77 + 120));
        v78 = *(_BYTE *)(v77 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v77 + 64)) != 0;
        if ( !v78 && *(_BYTE *)(v77 + 97) != 0 )
          sub_1412D33C0(v77);
      }
      else
      {
        MEMORY[0x141948990](v85 - *(unsigned int *)(qword_141ABD470 + 48));
      }
    }
    return 1;
  }
  if ( a2 > 1282567275 )
  {
    if ( a2 != 1282567276 )
    {
      if ( a2 != 1282893153 )
        return sub_140FE3F20((_DWORD *)a1, a2, a3);
      v14 = *(_QWORD *)(a1 + 104);
      if ( v14 != 0 )
      {
        v15 = *(_DWORD *)(v14 + 12);
        v16 = *(_DWORD *)(v14 + 16);
        if ( v16 == 0 )
          v16 = v15;
      }
      else
      {
        v15 = -1;
        v16 = -1;
      }
      v88 = __PAIR64__(v16, v15);
      v49 = 2004117618;
LABEL_58:
      sub_140FE72B0(&v88, v49, a3);
      return 1;
    }
    sub_1407C9510(&v88);
    v32 = *(_QWORD *)(a1 + 48);
    v33 = *(_QWORD *)(a1 + 56);
    v34 = v33 - v32;
    v35 = (v33 - v32) >> 4;
    v36 = v88;
    if ( (__int64)(v90 - v88) >> 3 >= v35 )
    {
      if ( v33 == v32 )
      {
LABEL_51:
        sub_14083DB80(&v85, &v88);
        v44 = *v3;
        if ( &v85 != v3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v44 + 16LL))(v44, v3);
          v47 = v85;
          v48 = v86;
          v3[1] = v86;
          *v3 = v47;
          v44 = sub_14083D4F0(v48) + 8;
          v86 = 0;
          v85 = v44;
        }
        goto LABEL_53;
      }
LABEL_72:
      v59 = 0;
      do
      {
        v60 = *(_QWORD *)(a1 + 48);
        if ( v60 != 0 )
        {
          v61 = sub_14083D4F0(v33);
          v86 = 0;
          v85 = v61 + 8;
          sub_14145B4C0(v59 + v60, &v85, 0);
          sub_14083B5F0(&v88, &v85);
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v85 + 16LL))(v85, &v85);
        }
        v59 += 16;
        --v35;
      }
      while ( v35 != 0 );
      goto LABEL_51;
    }
    v82 = v3;
    if ( v34 >= 0 )
    {
      v37 = v89;
      v38 = sub_1407E4490(qword_141ABD470, (unsigned __int64)v34 >> 1);
      sub_141758A00(v38, v88, v89 - v88);
      if ( v88 != 0 )
      {
        v39 = v90 - v88;
        if ( v90 - v88 == -1 )
          v39 = *(unsigned int *)(v88 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
          && (v40 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v40) >> 3 > v39)
          && (v41 = *(_QWORD *)(v40 + 8 * v39)) != 0 )
        {
          MEMORY[0x1419475D8](v41 + 32, v88 - *(unsigned int *)(v41 + 120));
          v42 = *(_BYTE *)(v41 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v41 + 64)) != 0;
          if ( !v42 && *(_BYTE *)(v41 + 97) != 0 )
            sub_1412D33C0(v41);
        }
        else
        {
          MEMORY[0x141948990](v88 - *(unsigned int *)(qword_141ABD470 + 48));
        }
      }
      v88 = v38;
      v89 = v38 + v37 - v36;
      v90 = v38 + 8 * v35;
      v3 = v82;
      goto LABEL_72;
    }
LABEL_124:
    sub_1400526C0(v33, v34);
  }
  if ( a2 == 1282302324 )
  {
    v17 = *(_QWORD *)(a1 + 96);
    if ( v17 != 0 )
    {
      v18 = *(_DWORD *)(v17 + 12);
      v19 = *(_DWORD *)(v17 + 16);
      if ( v19 == 0 )
        v19 = v18;
    }
    else
    {
      v18 = -1;
      v19 = -1;
    }
    v88 = __PAIR64__(v19, v18);
    v49 = 1315856756;
    goto LABEL_58;
  }
  if ( a2 != 1282436976 )
    return sub_140FE3F20((_DWORD *)a1, a2, a3);
  v5 = *(_DWORD *)(a1 + 112);
  v6 = sub_14083D4F0(a1) + 40;
  LODWORD(v89) = v5;
  v88 = v6;
  if ( &v88 != (unsigned __int64 *)v3 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v3 + 16LL))(*v3, v3);
    v7 = v88;
    v8 = v89;
    v3[1] = v89;
    *v3 = v7;
    v6 = sub_14083D4F0(v8) + 8;
    v89 = 0;
    v88 = v6;
  }
LABEL_7:
  (*(void (__fastcall **)(__int64, unsigned __int64 *))(*(_QWORD *)v6 + 16LL))(v6, &v88);
  return 1;
}
