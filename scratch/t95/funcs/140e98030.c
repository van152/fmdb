char __fastcall sub_140E98030(_QWORD *a1, __int64 *a2)
{
  __int64 v2; // rdi
  __int64 v4; // r15
  __int64 v5; // rbx
  __int64 v6; // rbx
  __int64 v7; // rcx
  __int64 v8; // rdx
  unsigned __int64 v9; // rsi
  __int64 v10; // r13
  __int64 v11; // r12
  __int64 v12; // r14
  unsigned __int64 v13; // rcx
  __int64 v14; // r8
  __int64 v15; // rcx
  __int64 v16; // rdi
  __int64 v17; // rdi
  __int64 v18; // rsi
  __int64 v19; // r14
  __int64 v20; // rax
  int v21; // ecx
  __int64 v22; // rcx
  __int64 v23; // rax
  __int64 v24; // rcx
  char result; // al
  unsigned __int64 v26; // rbx
  __int64 v27; // rcx
  __int64 v28; // rsi
  signed __int32 v29; // et0
  int v31[2]; // [rsp+30h] [rbp-40h] BYREF
  __int64 v32; // [rsp+38h] [rbp-38h]
  __int64 v33; // [rsp+40h] [rbp-30h]
  __int64 v34; // [rsp+48h] [rbp-28h] BYREF
  __int64 v35; // [rsp+50h] [rbp-20h]
  unsigned __int64 v36; // [rsp+58h] [rbp-18h]
  __int64 v37; // [rsp+60h] [rbp-10h] BYREF
  __int64 v38; // [rsp+68h] [rbp-8h]
  __int64 v39; // [rsp+70h] [rbp+0h]

  v39 = -2;
  v2 = a1[1] - *a1;
  if ( v2 != 0 )
  {
    if ( v2 < 0 )
      sub_1400526C0(a1);
    v4 = sub_1407E4490(qword_141ABD470, v2);
    v32 = v4 + 8 * (v2 >> 3);
    v5 = a1[1] - *a1;
    sub_141758A00();
    v6 = v4 + v5;
  }
  else
  {
    v4 = 0;
    v6 = 0;
    v32 = 0;
  }
  sub_1407C9510(&v34);
  v8 = v6 - v4;
  v9 = (v6 - v4) >> 3;
  v10 = v34;
  if ( (__int64)(v36 - v34) >> 3 < v9 )
  {
    if ( v8 < 0 )
      sub_1400526C0(v7);
    v11 = v35;
    v12 = sub_1407E4490(qword_141ABD470, v8);
    sub_141758A00();
    if ( v34 == 0 )
      goto LABEL_18;
    v13 = v36 - v34;
    if ( v36 - v34 == -1 )
    {
      v13 = *(unsigned int *)(v34 - *(unsigned int *)(qword_141ABD470 + 48));
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
        v16 = v34 - *(unsigned int *)(v15 + 120);
        v33 = v15;
        MEMORY[0x1419475D8](v15 + 32, v16);
        v7 = v33;
        if ( (*(_BYTE *)(v33 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v33 + 64)) == 0)
          && *(_BYTE *)(v33 + 97) != 0 )
        {
          sub_1412D33C0(v33);
        }
        goto LABEL_18;
      }
    }
LABEL_17:
    MEMORY[0x141948990](v34 - *(unsigned int *)(qword_141ABD470 + 48));
LABEL_18:
    v34 = v12;
    v35 = v12 + v11 - v10;
    v36 = v12 + 8 * v9;
  }
  if ( v6 != v4 )
  {
    v17 = 1;
    if ( v9 >= 2 )
      v17 = (v6 - v4) >> 3;
    v18 = 0;
    do
    {
      v19 = *(_QWORD *)(v4 + 8 * v18);
      if ( v19 != 0 )
      {
        v20 = sub_14083D4F0(v7);
        v38 = 0;
        v37 = v20 + 8;
        v21 = *(_DWORD *)(v19 + 16);
        if ( v21 == 0 )
          v21 = *(_DWORD *)(v19 + 12);
        v31[0] = *(_DWORD *)(v19 + 12);
        v31[1] = v21;
        sub_140FE72B0(v31, 1348825715, &v37);
        sub_14083B5F0(&v34, &v37);
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v37 + 16LL))(v37, &v37);
      }
      ++v18;
    }
    while ( v17 != v18 );
  }
  sub_14083DB80(&v37, &v34);
  v22 = *a2;
  if ( &v37 != a2 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v22 + 16LL))(v22, a2);
    v23 = v37;
    v24 = v38;
    a2[1] = v38;
    *a2 = v23;
    v22 = sub_14083D4F0(v24) + 8;
    v38 = 0;
    v37 = v22;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v22 + 16LL))(v22, &v37);
  result = sub_14083B0A0(&v34);
  if ( v4 != 0 )
  {
    v26 = v32 - v4;
    if ( v32 - v4 == -1 )
    {
      v26 = *(unsigned int *)(v4 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        return MEMORY[0x141948990](v4 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      return MEMORY[0x141948990](v4 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    v27 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v27) >> 3 <= v26 )
      return MEMORY[0x141948990](v4 - *(unsigned int *)(qword_141ABD470 + 48));
    v28 = *(_QWORD *)(v27 + 8 * v26);
    if ( v28 == 0 )
      return MEMORY[0x141948990](v4 - *(unsigned int *)(qword_141ABD470 + 48));
    MEMORY[0x1419475D8](v28 + 32, v4 - *(unsigned int *)(v28 + 120));
    if ( *(_BYTE *)(v28 + 72) != 0 )
    {
      v29 = _InterlockedDecrement((volatile signed __int32 *)(v28 + 64));
      result = v29 != 0;
      if ( v29 != 0 )
        return result;
    }
    else
    {
      result = 0;
    }
    if ( *(_BYTE *)(v28 + 97) != 0 )
      return sub_1412D33C0(v28);
  }
  return result;
}
