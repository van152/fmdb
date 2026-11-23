// THUNK ALIAS -> sub_143C81950 (jmp:0x140eb4030->0x143c81950)
__int64 __fastcall sub_143C81950(__int64 a1, __int64 *a2)
{
  __int64 v4; // rax
  __int64 *v5; // rcx
  __int64 v6; // rax
  __int64 v7; // rcx
  unsigned __int64 v8; // rbx
  __int64 v9; // r12
  __int64 v10; // rsi
  __int64 v11; // r14
  unsigned __int64 v12; // rcx
  __int64 v13; // r8
  __int64 v14; // rcx
  bool v15; // al
  __int64 v16; // rcx
  __int64 v17; // rax
  __int64 v18; // rcx
  __int64 v20; // rdi
  __int64 v21; // rax
  __int64 *v22; // rax
  __int64 v23; // rsi
  __int64 v24; // rax
  __int64 v25; // [rsp+20h] [rbp-30h]
  __int64 v26; // [rsp+28h] [rbp-28h] BYREF
  __int64 v27; // [rsp+30h] [rbp-20h]
  unsigned __int64 v28; // [rsp+38h] [rbp-18h]
  __int64 v29; // [rsp+40h] [rbp-10h] BYREF
  __int64 v30; // [rsp+48h] [rbp-8h]
  __int64 v31; // [rsp+50h] [rbp+0h]

  v31 = -2;
  sub_1407C9510(&v26);
  v4 = *(_QWORD *)(**(_QWORD **)a1 + 256LL);
  if ( v4 != 0 )
  {
    v5 = *(__int64 **)(v4 + 104);
    if ( v5 != nullptr )
    {
      v6 = *v5;
      v7 = v5[1];
      v8 = 0xAAAAAAAAAAAAAAABuLL * ((v7 - v6) >> 2);
      v9 = v26;
      if ( (__int64)(v28 - v26) >> 3 >= v8 )
      {
        if ( v7 == v6 )
          goto LABEL_14;
      }
      else
      {
        if ( v8 >> 61 != 0 )
          sub_1400526C0(v7);
        v10 = v27;
        v11 = sub_1407E4490(qword_141ABD470, 0x5555555555555558LL * ((v7 - v6) >> 2));
        sub_141758A00();
        if ( v26 != 0 )
        {
          v12 = v28 - v26;
          if ( v28 - v26 == -1 )
            v12 = *(unsigned int *)(v26 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v13 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v13) >> 3 > v12)
            && (v14 = *(_QWORD *)(v13 + 8 * v12)) != 0 )
          {
            v25 = v14;
            MEMORY[0x1419475D8](v14 + 32, v26 - *(unsigned int *)(v14 + 120));
            v7 = v25;
            v15 = *(_BYTE *)(v25 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v25 + 64)) != 0;
            if ( !v15 && *(_BYTE *)(v25 + 97) != 0 )
              sub_1412D33C0(v25);
          }
          else
          {
            MEMORY[0x141948990](v26 - *(unsigned int *)(qword_141ABD470 + 48));
          }
        }
        v26 = v11;
        v27 = v11 + v10 - v9;
        v28 = v11 + 8 * v8;
      }
      v20 = 0;
      do
      {
        v21 = *(_QWORD *)(**(_QWORD **)a1 + 256LL);
        if ( v21 != 0 )
        {
          v22 = *(__int64 **)(v21 + 104);
          if ( v22 != nullptr )
          {
            v23 = *v22;
            if ( *v22 != 0 )
            {
              v24 = sub_14083D4F0(v7);
              v30 = 0;
              v29 = v24 + 8;
              sub_140EADA20(v20 + v23, &v29);
              sub_14083B5F0(&v26, &v29);
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v29 + 16LL))(v29, &v29);
            }
          }
        }
        v20 += 12;
        --v8;
      }
      while ( v8 != 0 );
    }
  }
LABEL_14:
  sub_14083DB80(&v29, &v26);
  v16 = *a2;
  if ( &v29 != a2 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v16 + 16LL))(v16, a2);
    v17 = v29;
    v18 = v30;
    a2[1] = v30;
    *a2 = v17;
    v16 = sub_14083D4F0(v18) + 8;
    v30 = 0;
    v29 = v16;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v16 + 16LL))(v16, &v29);
  return sub_14083B0A0(&v26);
}
