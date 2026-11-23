char __fastcall sub_140ECB110(_QWORD *a1, __int64 *a2)
{
  __int64 v3; // rsi
  __int64 v4; // r15
  __int64 v5; // rdi
  __int64 *v6; // rcx
  __int64 v7; // rax
  __int64 v8; // rcx
  unsigned __int64 v9; // r12
  __int64 v10; // r14
  __int64 v11; // r13
  __int64 v12; // rbx
  unsigned __int64 v13; // rcx
  __int64 v14; // rcx
  __int64 v15; // rax
  __int64 v16; // rcx
  char result; // al
  unsigned __int64 v18; // rbx
  __int64 v19; // rcx
  __int64 v20; // rdi
  signed __int32 v21; // et0
  __int64 v22; // r8
  __int64 v23; // rcx
  bool v24; // al
  __int64 v25; // r14
  __int64 *v26; // rax
  __int64 v27; // rsi
  __int64 v28; // rax
  __int64 v30; // [rsp+28h] [rbp-38h]
  __int64 v31; // [rsp+30h] [rbp-30h]
  __int64 v32; // [rsp+38h] [rbp-28h] BYREF
  __int64 v33; // [rsp+40h] [rbp-20h]
  unsigned __int64 v34; // [rsp+48h] [rbp-18h]
  __int64 v35; // [rsp+50h] [rbp-10h] BYREF
  __int64 v36; // [rsp+58h] [rbp-8h]
  __int64 v37; // [rsp+60h] [rbp+0h]

  v37 = -2;
  v3 = a1[1] - *a1;
  if ( v3 != 0 )
  {
    if ( v3 < 0 )
      sub_1400526C0(a1);
    v4 = sub_1407E4490(qword_141ABD470, v3);
    v30 = v4 + 8 * (v3 >> 3);
    sub_141758A00();
  }
  else
  {
    v4 = 0;
    v30 = 0;
  }
  v5 = a1[3];
  sub_1407C9510(&v32);
  v6 = *(__int64 **)(v5 + 256);
  if ( v6 != nullptr )
  {
    v7 = *v6;
    v8 = v6[1];
    v9 = 0xAAAAAAAAAAAAAAABuLL * ((v8 - v7) >> 1);
    v10 = v32;
    if ( (__int64)(v34 - v32) >> 3 >= v9 )
    {
      if ( v8 == v7 )
        goto LABEL_13;
      goto LABEL_34;
    }
    if ( v9 >> 61 != 0 )
      sub_1400526C0(v8);
    v11 = v33;
    v12 = sub_1407E4490(qword_141ABD470, 0x5555555555555558LL * ((v8 - v7) >> 1));
    sub_141758A00();
    if ( v32 == 0 )
    {
LABEL_33:
      v32 = v12;
      v33 = v12 + v11 - v10;
      v34 = v12 + 8 * v9;
LABEL_34:
      v25 = 0;
      do
      {
        v26 = *(__int64 **)(v5 + 256);
        if ( v26 != nullptr )
        {
          v27 = *v26;
          if ( *v26 != 0 )
          {
            v28 = sub_14083D4F0(v8);
            v36 = 0;
            v35 = v28 + 8;
            sub_140ED2AC0(v25 + v27, &v35);
            sub_14083B5F0(&v32, &v35);
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v35 + 16LL))(v35, &v35);
          }
        }
        v25 += 6;
        --v9;
      }
      while ( v9 != 0 );
      goto LABEL_13;
    }
    v13 = v34 - v32;
    if ( v34 - v32 == -1 )
    {
      v13 = *(unsigned int *)(v32 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
LABEL_32:
        MEMORY[0x141948990](v32 - *(unsigned int *)(qword_141ABD470 + 48));
        goto LABEL_33;
      }
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      goto LABEL_32;
    }
    v22 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v22) >> 3 > v13 )
    {
      v23 = *(_QWORD *)(v22 + 8 * v13);
      if ( v23 != 0 )
      {
        v31 = v23;
        MEMORY[0x1419475D8](v23 + 32, v32 - *(unsigned int *)(v23 + 120));
        v8 = v31;
        v24 = *(_BYTE *)(v31 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v31 + 64)) != 0;
        if ( !v24 && *(_BYTE *)(v31 + 97) != 0 )
          sub_1412D33C0(v31);
        goto LABEL_33;
      }
    }
    goto LABEL_32;
  }
LABEL_13:
  sub_14083DB80(&v35, &v32);
  v14 = *a2;
  if ( &v35 != a2 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v14 + 16LL))(v14, a2);
    v15 = v35;
    v16 = v36;
    a2[1] = v36;
    *a2 = v15;
    v14 = sub_14083D4F0(v16) + 8;
    v36 = 0;
    v35 = v14;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v14 + 16LL))(v14, &v35);
  result = sub_14083B0A0(&v32);
  if ( v4 != 0 )
  {
    v18 = v30 - v4;
    if ( v30 - v4 == -1 )
    {
      v18 = *(unsigned int *)(v4 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        return MEMORY[0x141948990](v4 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      return MEMORY[0x141948990](v4 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    v19 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v19) >> 3 <= v18 )
      return MEMORY[0x141948990](v4 - *(unsigned int *)(qword_141ABD470 + 48));
    v20 = *(_QWORD *)(v19 + 8 * v18);
    if ( v20 == 0 )
      return MEMORY[0x141948990](v4 - *(unsigned int *)(qword_141ABD470 + 48));
    MEMORY[0x1419475D8](v20 + 32, v4 - *(unsigned int *)(v20 + 120));
    if ( *(_BYTE *)(v20 + 72) != 0 )
    {
      v21 = _InterlockedDecrement((volatile signed __int32 *)(v20 + 64));
      result = v21 != 0;
      if ( v21 != 0 )
        return result;
    }
    else
    {
      result = 0;
    }
    if ( *(_BYTE *)(v20 + 97) != 0 )
      return sub_1412D33C0(v20);
  }
  return result;
}
