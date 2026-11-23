char __fastcall sub_1410C4E30(__int64 *a1, char a2, __int64 *a3)
{
  __int64 v4; // rbx
  __int64 v5; // rcx
  __int64 v6; // r15
  unsigned __int8 v7; // r13
  unsigned __int8 v8; // r12
  __int64 v9; // r14
  __int64 v10; // rax
  int v11; // ecx
  int v12; // ecx
  int v13; // ecx
  int v14; // eax
  _QWORD *v15; // rsi
  __int64 v16; // rcx
  __int64 v17; // rcx
  __int64 v18; // rcx
  __int64 v19; // r15
  __int64 v20; // rsi
  __int64 v21; // rdi
  unsigned __int64 v22; // rcx
  __int64 v23; // rbx
  __int64 v24; // rax
  int v25; // ecx
  int v26; // ecx
  int v27; // ecx
  bool v28; // cf
  _QWORD *v29; // rsi
  __int64 v30; // rcx
  __int64 v31; // rdx
  __int64 v32; // rcx
  __int64 v33; // r8
  __int64 v34; // r14
  __int64 v35; // rax
  __int64 v36; // rcx
  __int64 v37; // rax
  __int64 v38; // rcx
  __int64 v39; // rax
  __int64 v40; // rcx
  __int64 v41; // rax
  __int64 v42; // rcx
  __int64 v43; // rax
  __int64 v44; // rcx
  __int64 v45; // rax
  __int64 v46; // rcx
  __int64 v47; // rax
  __int64 v48; // rcx
  __int64 v49; // rax
  __int64 v50; // rcx
  __int64 v51; // rax
  __int64 v52; // rcx
  __int64 v55; // [rsp+28h] [rbp-58h]
  __int64 v56; // [rsp+30h] [rbp-50h] BYREF
  __int64 v57; // [rsp+38h] [rbp-48h]
  __int64 v58; // [rsp+40h] [rbp-40h] BYREF
  __int64 v59; // [rsp+48h] [rbp-38h]
  __int64 v60; // [rsp+50h] [rbp-30h]
  __int64 v61; // [rsp+58h] [rbp-28h] BYREF
  int v62; // [rsp+60h] [rbp-20h]
  int v63; // [rsp+70h] [rbp-10h]
  int v64; // [rsp+74h] [rbp-Ch]
  int v65; // [rsp+78h] [rbp-8h]
  int v66; // [rsp+7Ch] [rbp-4h]
  __int64 v67; // [rsp+80h] [rbp+0h]

  v67 = -2;
  v4 = a1[1];
  v5 = *a1;
  v55 = (v4 - v5) >> 3;
  if ( v4 == v5 )
  {
    v7 = 0;
    v8 = 0;
    v65 = 0;
    v64 = 0;
    v63 = 0;
    v66 = 0;
  }
  else
  {
    v6 = 1;
    if ( (unsigned __int64)((v4 - v5) >> 3) >= 2 )
      v6 = (v4 - v5) >> 3;
    if ( a2 != 0 )
    {
      v7 = 0;
      v8 = 0;
      v65 = 0;
      v64 = 0;
      v63 = 0;
      v66 = 0;
      v9 = 0;
      do
      {
        v15 = *(_QWORD **)(*a1 + 8 * v9);
        if ( v15 != nullptr )
        {
          v16 = (__int64)v15 + *(int *)(v15[1] + 4LL) + 8;
          if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v16 + 1312LL))(v16) == 0
            || (v17 = (__int64)v15 + *(int *)(v15[1] + 4LL) + 8,
                *(char *)((*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v17 + 1832LL))(v17) + 30) >= 0) )
          {
            v10 = (*(__int64 (__fastcall **)(_QWORD *))(*v15 + 800LL))(v15);
            sub_14085D840(v10, &v58, 0);
            v7 += v58 & 1;
            v8 -= ((v58 & 0x1C) == 0) - 1;
            v11 = v65;
            LOBYTE(v11) = v65 - (((v58 & 0xE0) == 0) - 1);
            v65 = v11;
            v12 = v64;
            LOBYTE(v12) = v64 - (((v58 & 0x700) == 0) - 1);
            v64 = v12;
            v13 = v63;
            LOBYTE(v13) = v63 - (((v58 & 0x3800) == 0) - 1);
            v63 = v13;
            v14 = v66;
            LOBYTE(v14) = v66 - (((v58 & 0x1C000) == 0) - 1);
            v66 = v14;
          }
        }
        ++v9;
      }
      while ( v6 != v9 );
    }
    else
    {
      v7 = 0;
      v8 = 0;
      v65 = 0;
      v64 = 0;
      v63 = 0;
      v66 = 0;
      v23 = 0;
      do
      {
        v29 = *(_QWORD **)(*a1 + 8 * v23);
        if ( v29 != nullptr )
        {
          v30 = (__int64)v29 + *(int *)(v29[1] + 4LL) + 8;
          if ( (*(unsigned __int8 (__fastcall **)(__int64))(*(_QWORD *)v30 + 1312LL))(v30) == 0
            || (v32 = (__int64)v29 + *(int *)(v29[1] + 4LL) + 8,
                *(char *)((*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v32 + 1832LL))(v32) + 30) >= 0) )
          {
            LOBYTE(v31) = 15;
            v24 = (*(__int64 (__fastcall **)(_QWORD *, __int64))(*v29 + 1128LL))(v29, v31);
            v7 += v24 & 1;
            v8 -= ((v24 & 0x1C) == 0) - 1;
            v25 = v65;
            LOBYTE(v25) = v65 - (((v24 & 0xE0) == 0) - 1);
            v65 = v25;
            v26 = v64;
            LOBYTE(v26) = v64 - (((v24 & 0x700) == 0) - 1);
            v64 = v26;
            v27 = v63;
            LOBYTE(v27) = v63 - (((v24 & 0x3800) == 0) - 1);
            v63 = v27;
            v28 = (v24 & 0x1C000) == 0;
            LODWORD(v24) = v66;
            LOBYTE(v24) = v66 - (v28 - 1);
            v66 = v24;
          }
        }
        ++v23;
      }
      while ( v6 != v23 );
    }
  }
  sub_1407C9510(&v58);
  v19 = v58;
  if ( (unsigned __int64)(v60 - v58) <= 0x37 )
  {
    v20 = v59;
    v21 = sub_1407E4490(qword_141ABD470, 56);
    sub_141758A00();
    if ( v58 == 0 )
    {
LABEL_32:
      v58 = v21;
      v59 = v21 + v20 - v19;
      v60 = v21 + 56;
      goto LABEL_33;
    }
    v22 = v60 - v58;
    if ( v60 - v58 == -1 )
    {
      v22 = *(unsigned int *)(v58 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_31:
        MEMORY[0x141948990](v58 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_32;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_31;
    }
    v33 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v33) >> 3 > v22 )
    {
      v34 = *(_QWORD *)(v33 + 8 * v22);
      if ( v34 != 0 )
      {
        MEMORY[0x1419475D8](v34 + 32, v58 - *(unsigned int *)(v34 + 120));
        if ( (*(_BYTE *)(v34 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v34 + 64)) == 0)
          && *(_BYTE *)(v34 + 97) != 0 )
        {
          sub_1412D33C0(v34);
        }
        goto LABEL_32;
      }
    }
    goto LABEL_31;
  }
LABEL_33:
  v35 = sub_14083D4F0(v18);
  v62 = v7;
  v61 = v35 + 56;
  sub_14083B5F0(&v58, &v61);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v61 + 16LL))(v61, &v61);
  v37 = sub_14083D4F0(v36);
  v62 = 0;
  v61 = v37 + 56;
  sub_14083B5F0(&v58, &v61);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v61 + 16LL))(v61, &v61);
  v39 = sub_14083D4F0(v38);
  v62 = v8;
  v61 = v39 + 56;
  sub_14083B5F0(&v58, &v61);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v61 + 16LL))(v61, &v61);
  v41 = sub_14083D4F0(v40);
  v62 = (unsigned __int8)v65;
  v61 = v41 + 56;
  sub_14083B5F0(&v58, &v61);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v61 + 16LL))(v61, &v61);
  v43 = sub_14083D4F0(v42);
  v62 = (unsigned __int8)v64;
  v61 = v43 + 56;
  sub_14083B5F0(&v58, &v61);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v61 + 16LL))(v61, &v61);
  v45 = sub_14083D4F0(v44);
  v62 = (unsigned __int8)v63;
  v61 = v45 + 56;
  sub_14083B5F0(&v58, &v61);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v61 + 16LL))(v61, &v61);
  v47 = sub_14083D4F0(v46);
  v62 = (unsigned __int8)v66;
  v61 = v47 + 56;
  sub_14083B5F0(&v58, &v61);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v61 + 16LL))(v61, &v61);
  sub_1407C9510(&v61);
  sub_14083DB80(&v56, &v58);
  sub_140833EB0(&v61, 1347180867, &v56);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v56 + 16LL))(v56, &v56);
  v49 = sub_14083D4F0(v48);
  v57 = v55;
  v56 = v49 + 88;
  sub_140833EB0(&v61, 1347178563, &v56);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v56 + 16LL))(v56, &v56);
  sub_14083DDA0(&v56, &v61);
  v50 = *a3;
  if ( &v56 != a3 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v50 + 16LL))(v50, a3);
    v51 = v56;
    v52 = v57;
    a3[1] = v57;
    *a3 = v51;
    v50 = sub_14083D4F0(v52) + 8;
    v57 = 0;
    v56 = v50;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v50 + 16LL))(v50, &v56);
  sub_140833970(&v61);
  sub_14083B0A0(&v58);
  return 1;
}
