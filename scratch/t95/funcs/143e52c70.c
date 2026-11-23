__int64 __fastcall sub_143E52C70(__int64 a1, int a2, volatile signed __int32 **a3)
{
  char *v6; // rdx
  __int64 v7; // rsi
  unsigned __int64 v9; // rsi
  __int64 v10; // rbx
  char *v11; // rax
  char *v12; // r8
  char *v13; // rax
  unsigned __int64 v14; // rbx
  __int64 v15; // rdx
  volatile signed __int32 **v16; // rsi
  volatile signed __int32 *v17; // rdx
  volatile signed __int32 *v18; // rax
  volatile signed __int32 *v19; // rcx
  volatile signed __int32 *v20; // rdi
  volatile signed __int32 *v21; // rdi
  __int64 v22; // rbx
  __int64 v23; // rcx
  _DWORD v24[2]; // [rsp+20h] [rbp-60h] BYREF
  __int64 v25; // [rsp+28h] [rbp-58h]
  __int64 v26; // [rsp+30h] [rbp-50h]
  __int64 v27; // [rsp+38h] [rbp-48h]
  __int64 v28; // [rsp+40h] [rbp-40h]
  __int64 v29; // [rsp+48h] [rbp-38h]
  __int64 v30; // [rsp+50h] [rbp-30h]
  __int64 v31; // [rsp+58h] [rbp-28h]
  __int64 v32; // [rsp+60h] [rbp-20h]
  __int64 v33; // [rsp+68h] [rbp-18h]
  __int64 v34; // [rsp+70h] [rbp-10h]
  __int64 v35; // [rsp+78h] [rbp-8h]
  __int64 v36; // [rsp+80h] [rbp+0h]
  __int64 v37; // [rsp+88h] [rbp+8h]
  __int64 v38; // [rsp+90h] [rbp+10h]
  __int64 v39; // [rsp+98h] [rbp+18h]
  __int64 v40; // [rsp+A0h] [rbp+20h]
  __int64 v41; // [rsp+A8h] [rbp+28h]
  __int64 v42; // [rsp+B0h] [rbp+30h]
  int v43; // [rsp+B8h] [rbp+38h]
  __int64 v44; // [rsp+C0h] [rbp+40h]

  v44 = -2;
  v24[0] = -1;
  v25 = 0;
  v26 = 0;
  v27 = 0;
  if ( qword_141ABD470 == 0 )
  {
    if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B59AA8);
      if ( dword_141B59AA8 == -1 )
      {
        sub_1407E3E70(&unk_141B59A68);
        sub_141751048(sub_1407E4B20);
        sub_141750EA0(&dword_141B59AA8);
      }
    }
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  v43 = 0;
  v42 = 0;
  v41 = 0;
  v40 = 0;
  v39 = 0;
  v38 = 0;
  v37 = 0;
  v36 = 0;
  v35 = 0;
  v34 = 0;
  v33 = 0;
  v32 = 0;
  v31 = 0;
  v30 = 0;
  v29 = 0;
  v28 = 0;
  v24[1] = a2;
  v6 = *(char **)(a1 + 32);
  v7 = *(_QWORD *)(a1 + 40) - (_QWORD)v6;
  if ( v7 >= 8 )
  {
    v9 = (unsigned __int64)v7 >> 3;
    v10 = v9;
    do
    {
      v10 = (unsigned __int64)v10 >> 1;
      v11 = &v6[8 * v10];
      if ( *(_DWORD *)(*(_QWORD *)v11 + 4LL) < a2 )
      {
        v10 = v9 + ~v10;
        v6 = v11 + 8;
      }
      else if ( *(_DWORD *)(*(_QWORD *)v11 + 4LL) <= a2 )
      {
        v12 = v6;
        if ( v9 >= 2 )
        {
          v22 = v10 & 0x1FFFFFFFFFFFFFFFLL;
          v12 = v6;
          v23 = v22;
          do
          {
            v23 = (unsigned __int64)v23 >> 1;
            if ( *(_DWORD *)(*(_QWORD *)&v12[8 * v23] + 4LL) < a2 )
            {
              v12 += 8 * v23 + 8;
              v23 = v22 + ~v23;
            }
            v22 = v23;
          }
          while ( v23 > 0 );
        }
        v13 = v11 + 8;
        if ( &v6[8 * v9] - v13 > 0 )
        {
          v14 = (unsigned __int64)(&v6[8 * v9] - v13) >> 3;
          v15 = v14;
          do
          {
            v15 = (unsigned __int64)v15 >> 1;
            if ( *(_DWORD *)(*(_QWORD *)&v13[8 * v15] + 4LL) <= a2 )
            {
              v13 += 8 * v15 + 8;
              v15 = v14 + ~v15;
            }
            v14 = v15;
          }
          while ( v15 > 0 );
        }
        if ( v12 != v13 )
        {
          v16 = (volatile signed __int32 **)(*(_QWORD *)v12 + 8LL);
          if ( v16 != a3 )
          {
            v17 = *a3;
            v18 = *v16;
            v19 = *v16 - 1;
            if ( *v16 == nullptr )
              v19 = nullptr;
            v20 = v17 - 1;
            if ( v17 != nullptr )
            {
              if ( v18 != nullptr && _InterlockedDecrement(v19) == 0 )
                sub_1412EC9A0((__int64)v19);
              *v16 = nullptr;
              _InterlockedIncrement(v20);
              v21 = v20 + 1;
            }
            else
            {
              if ( v18 != nullptr && _InterlockedDecrement(v19) == 0 )
                sub_1412EC9A0((__int64)v19);
              v21 = nullptr;
            }
            *v16 = v21;
          }
        }
        return sub_140FF5030(v24);
      }
      v9 = v10;
    }
    while ( v10 > 0 );
  }
  return sub_140FF5030(v24);
}
