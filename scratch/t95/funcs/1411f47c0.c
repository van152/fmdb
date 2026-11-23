char __fastcall sub_1411F47C0(_QWORD *a1, __int64 *a2)
{
  __int64 v3; // rsi
  __int64 v4; // r15
  __int64 v5; // rdi
  __int64 v6; // rax
  __int64 *v7; // rcx
  __int64 v8; // rax
  __int64 v9; // rcx
  __int64 v10; // rdx
  unsigned __int64 v11; // r12
  __int64 v12; // r14
  __int64 v13; // r13
  __int64 v14; // rbx
  unsigned __int64 v15; // rcx
  __int64 v16; // r8
  __int64 v17; // rcx
  bool v18; // al
  __int64 v19; // rcx
  __int64 v20; // rax
  __int64 v21; // rcx
  char result; // al
  unsigned __int64 v23; // rbx
  __int64 v24; // rcx
  __int64 v25; // rdi
  signed __int32 v26; // et0
  __int64 v27; // r14
  __int64 v28; // rax
  _QWORD *v29; // rax
  __int64 v30; // rsi
  __int64 v31; // rax
  __int64 v33; // [rsp+28h] [rbp-38h]
  __int64 v34; // [rsp+30h] [rbp-30h]
  __int64 v35; // [rsp+38h] [rbp-28h] BYREF
  __int64 v36; // [rsp+40h] [rbp-20h]
  unsigned __int64 v37; // [rsp+48h] [rbp-18h]
  __int64 v38; // [rsp+50h] [rbp-10h] BYREF
  __int64 v39; // [rsp+58h] [rbp-8h]
  __int64 v40; // [rsp+60h] [rbp+0h]

  v40 = -2;
  v3 = a1[1] - *a1;
  if ( v3 != 0 )
  {
    if ( v3 < 0 )
      sub_1400526C0(a1);
    v4 = sub_1407E4490(qword_141ABD470, v3);
    v33 = v4 + 8 * (v3 >> 3);
    sub_141758A00();
  }
  else
  {
    v4 = 0;
    v33 = 0;
  }
  v5 = a1[3];
  sub_1407C9510(&v35);
  v6 = *(_QWORD *)(v5 + 176);
  if ( v6 != 0 )
  {
    v7 = *(__int64 **)(v6 + 72);
    if ( v7 != nullptr )
    {
      v8 = *v7;
      v9 = v7[1];
      v10 = v9 - v8;
      v11 = (v9 - v8) >> 3;
      v12 = v35;
      if ( (__int64)(v37 - v35) >> 3 >= v11 )
      {
        if ( v9 == v8 )
          goto LABEL_18;
      }
      else
      {
        if ( v10 < 0 )
          sub_1400526C0(v9);
        v13 = v36;
        v14 = sub_1407E4490(qword_141ABD470, v10);
        sub_141758A00();
        if ( v35 != 0 )
        {
          v15 = v37 - v35;
          if ( v37 - v35 == -1 )
            v15 = *(unsigned int *)(v35 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v16 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v16) >> 3 > v15)
            && (v17 = *(_QWORD *)(v16 + 8 * v15)) != 0 )
          {
            v34 = v17;
            MEMORY[0x1419475D8](v17 + 32, v35 - *(unsigned int *)(v17 + 120));
            v9 = v34;
            v18 = *(_BYTE *)(v34 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v34 + 64)) != 0;
            if ( !v18 && *(_BYTE *)(v34 + 97) != 0 )
              sub_1412D33C0(v34);
          }
          else
          {
            MEMORY[0x141948990](v35 - *(unsigned int *)(qword_141ABD470 + 48));
          }
        }
        v35 = v14;
        v36 = v14 + v13 - v12;
        v37 = v14 + 8 * v11;
      }
      v27 = 0;
      do
      {
        v28 = *(_QWORD *)(v5 + 176);
        if ( v28 != 0 )
        {
          v29 = *(_QWORD **)(v28 + 72);
          if ( v29 != nullptr )
          {
            v30 = *(_QWORD *)(*v29 + 8 * v27);
            if ( v30 != 0 )
            {
              v31 = sub_14083D4F0(v9);
              v39 = 0;
              v38 = v31 + 8;
              sub_1411FCF00(v30, &v38);
              sub_14083B5F0(&v35, &v38);
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v38 + 16LL))(v38, &v38);
            }
          }
        }
        ++v27;
      }
      while ( v11 != v27 );
    }
  }
LABEL_18:
  sub_14083DB80(&v38, &v35);
  v19 = *a2;
  if ( &v38 != a2 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v19 + 16LL))(v19, a2);
    v20 = v38;
    v21 = v39;
    a2[1] = v39;
    *a2 = v20;
    v19 = sub_14083D4F0(v21) + 8;
    v39 = 0;
    v38 = v19;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v19 + 16LL))(v19, &v38);
  result = sub_14083B0A0(&v35);
  if ( v4 != 0 )
  {
    v23 = v33 - v4;
    if ( v33 - v4 == -1 )
    {
      v23 = *(unsigned int *)(v4 - *(unsigned int *)(qword_141ABD470 + 48));
      if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        return MEMORY[0x141948990](v4 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
      return MEMORY[0x141948990](v4 - *(unsigned int *)(qword_141ABD470 + 48));
    }
    v24 = *(_QWORD *)(qword_141ABD470 + 24);
    if ( (*(_QWORD *)(qword_141ABD470 + 32) - v24) >> 3 <= v23 )
      return MEMORY[0x141948990](v4 - *(unsigned int *)(qword_141ABD470 + 48));
    v25 = *(_QWORD *)(v24 + 8 * v23);
    if ( v25 == 0 )
      return MEMORY[0x141948990](v4 - *(unsigned int *)(qword_141ABD470 + 48));
    MEMORY[0x1419475D8](v25 + 32, v4 - *(unsigned int *)(v25 + 120));
    if ( *(_BYTE *)(v25 + 72) != 0 )
    {
      v26 = _InterlockedDecrement((volatile signed __int32 *)(v25 + 64));
      result = v26 != 0;
      if ( v26 != 0 )
        return result;
    }
    else
    {
      result = 0;
    }
    if ( *(_BYTE *)(v25 + 97) != 0 )
      return sub_1412D33C0(v25);
  }
  return result;
}
