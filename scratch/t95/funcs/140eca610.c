char __fastcall sub_140ECA610(_QWORD *a1, __int64 *a2)
{
  __int64 v2; // rdi
  __int64 v4; // r15
  __int64 v5; // rsi
  __int64 v6; // rsi
  __int64 v7; // rdx
  unsigned __int64 v8; // rcx
  __int64 v9; // rbx
  unsigned __int64 v10; // r14
  __int64 v11; // r13
  __int64 v12; // r12
  unsigned __int64 v13; // rcx
  __int64 v14; // r8
  unsigned __int64 v15; // rcx
  __int64 v16; // rdi
  __int64 v17; // r12
  __int64 v18; // r14
  __int64 v19; // rax
  __int64 v20; // rdi
  __int64 v21; // rbx
  unsigned __int64 v22; // r13
  __int64 i; // rdi
  __int64 *v24; // rdx
  unsigned int v25; // r15d
  __int64 v26; // rcx
  __int64 v27; // rax
  __int64 v28; // rax
  __int64 v29; // rcx
  __int64 v30; // rax
  __int64 v31; // rcx
  char result; // al
  unsigned __int64 v33; // rdi
  __int64 v34; // rcx
  __int64 v35; // rsi
  signed __int32 v36; // et0
  __int64 v37; // [rsp+28h] [rbp-58h]
  __int64 v39[3]; // [rsp+38h] [rbp-48h] BYREF
  __int64 v40; // [rsp+50h] [rbp-30h]
  __int64 v41; // [rsp+58h] [rbp-28h] BYREF
  __int64 v42; // [rsp+60h] [rbp-20h]
  __int64 v43; // [rsp+68h] [rbp-18h] BYREF
  __int64 v44; // [rsp+70h] [rbp-10h]
  __int64 v45; // [rsp+80h] [rbp+0h] BYREF
  __int64 v46; // [rsp+88h] [rbp+8h]
  __int64 v47; // [rsp+90h] [rbp+10h] BYREF
  __int64 v48; // [rsp+98h] [rbp+18h]
  unsigned __int64 v49; // [rsp+A0h] [rbp+20h]
  unsigned __int64 v50; // [rsp+A8h] [rbp+28h]
  __int64 v51; // [rsp+B0h] [rbp+30h]

  v51 = -2;
  v2 = a1[1] - *a1;
  if ( v2 != 0 )
  {
    if ( v2 < 0 )
      sub_1400526C0(a1);
    v4 = sub_1407E4490(qword_141ABD470, v2);
    v40 = v4 + 8 * (v2 >> 3);
    v5 = a1[1] - *a1;
    sub_141758A00();
    v6 = v4 + v5;
  }
  else
  {
    v4 = 0;
    v6 = 0;
    v40 = 0;
  }
  sub_1407C9510(&v47);
  v7 = v6 - v4;
  v8 = (v6 - v4) >> 3;
  v9 = v47;
  v10 = v8;
  if ( (__int64)(v49 - v47) >> 3 < v8 )
  {
    if ( v7 < 0 )
      sub_1400526C0(v8);
    v11 = v48;
    v12 = sub_1407E4490(qword_141ABD470, v7);
    sub_141758A00();
    if ( v47 == 0 )
      goto LABEL_18;
    v13 = v49 - v47;
    if ( v49 - v47 == -1 )
    {
      v13 = *(unsigned int *)(v47 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        goto LABEL_17;
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_17;
    }
    v14 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v14) >> 3 > v13 )
    {
      v15 = *(_QWORD *)(v14 + 8 * v13);
      if ( v15 != 0 )
      {
        v16 = v47 - *(unsigned int *)(v15 + 120);
        v50 = v15;
        MEMORY[0x1419475D8](v15 + 32, v16);
        v8 = v50;
        if ( (*(_BYTE *)(v50 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v50 + 64)) == 0)
          && *(_BYTE *)(v8 + 97) != 0 )
        {
          sub_1412D33C0(v8);
        }
        goto LABEL_18;
      }
    }
LABEL_17:
    MEMORY[0x141948990](v47 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_18:
    v47 = v12;
    v48 = v12 + v11 - v9;
    v49 = v12 + 8 * v10;
  }
  if ( v6 != v4 )
  {
    if ( v10 < 2 )
      v10 = 1;
    v50 = v10;
    v17 = 0;
    v37 = v4;
    do
    {
      v18 = *(_QWORD *)(v4 + 8 * v17);
      if ( v18 != 0 )
      {
        v19 = sub_14083D4F0(v8);
        v42 = 0;
        v41 = v19 + 8;
        sub_1407C9510(&v43);
        sub_141563840(&v43);
        sub_1407C9510(v39);
        v20 = v43;
        v21 = v44;
        v22 = (v44 - v43) >> 3;
        if ( (v39[2] - v39[0]) >> 4 < v22 )
        {
          if ( (unsigned __int64)(v44 - v43) >= 0x7FFFFFFFFFFFFFF9LL )
            sub_1400526C0(0x7FFFFFFFFFFFFFF9LL);
          sub_140837DD0(v39, (v44 - v43) >> 3);
        }
        if ( v21 != v20 )
        {
          if ( v22 < 2 )
            v22 = 1;
          for ( i = 0; i != v22; ++i )
          {
            v24 = *(__int64 **)(v43 + 8 * i);
            if ( v24 == nullptr )
              v24 = &qword_141B5A4A0;
            v25 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v24 + 80LL))(*v24);
            v27 = sub_14083D4F0(v26);
            v46 = 0;
            v45 = v27 + 8;
            if ( (unsigned __int8)sub_14119D0F0(v18, v25, &v45) != 0 )
              sub_140835380(v39, v25, &v45);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v45 + 16LL))(v45, &v45);
          }
        }
        sub_14083DDA0(&v45, v39);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v41 + 16LL))(v41, &v41);
        v42 = v46;
        v41 = v45;
        v28 = sub_14083D4F0(v46);
        v46 = 0;
        v45 = v28 + 8;
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)(v28 + 8) + 16LL))(v28 + 8, &v45);
        v4 = v37;
        sub_140833970(v39);
        sub_14083B0A0(&v43);
        sub_14083B5F0(&v47, &v41);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v41 + 16LL))(v41, &v41);
      }
      ++v17;
    }
    while ( v17 != v50 );
  }
  sub_14083DB80(&v43, &v47);
  v29 = *a2;
  if ( &v43 != a2 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v29 + 16LL))(v29, a2);
    v30 = v43;
    v31 = v44;
    a2[1] = v44;
    *a2 = v30;
    v29 = sub_14083D4F0(v31) + 8;
    v44 = 0;
    v43 = v29;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v29 + 16LL))(v29, &v43);
  result = sub_14083B0A0(&v47);
  if ( v4 != 0 )
  {
    v33 = v40 - v4;
    if ( v40 - v4 == -1 )
    {
      v33 = *(unsigned int *)(v4 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        return MEMORY[0x141948990](v4 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      return MEMORY[0x141948990](v4 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    v34 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v34) >> 3 <= v33 )
      return MEMORY[0x141948990](v4 - *(unsigned int *)(qword_141ABD470 + 48));
    v35 = *(_QWORD *)(v34 + 8 * v33);
    if ( v35 == 0 )
      return MEMORY[0x141948990](v4 - *(unsigned int *)(qword_141ABD470 + 48));
    MEMORY[0x1419475D8](v35 + 32, v4 - *(unsigned int *)(v35 + 120));
    if ( *(_BYTE *)(v35 + 72) != 0 )
    {
      v36 = _InterlockedDecrement((volatile signed __int32 *)(v35 + 64));
      result = v36 != 0;
      if ( v36 != 0 )
        return result;
    }
    else
    {
      result = 0;
    }
    if ( *(_BYTE *)(v35 + 97) != 0 )
      return sub_1412D33C0(v35);
  }
  return result;
}
