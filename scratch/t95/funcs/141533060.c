// THUNK ALIAS -> sub_1444CF180 (jmp:0x141533060->0x1444cf180)
volatile signed __int32 **__fastcall sub_1444CF180(__int64 a1, volatile signed __int32 **a2)
{
  __int64 v4; // rax
  __int64 v5; // rcx
  unsigned __int64 v6; // rbx
  __int64 v7; // rbp
  volatile signed __int32 *v8; // rax
  __int64 v9; // r8
  volatile signed __int32 *v10; // rcx
  volatile signed __int32 *v11; // rbp
  volatile signed __int32 *v12; // rbp
  __int64 v13; // rdx
  __int64 v14; // rcx
  char v16; // [rsp+2Fh] [rbp-49h] BYREF
  _QWORD v17[9]; // [rsp+30h] [rbp-48h] BYREF

  *a2 = nullptr;
  v4 = *(_QWORD *)(a1 + 24);
  v5 = *(_QWORD *)(v4 + 280);
  if ( *(_QWORD *)(v4 + 288) != v5 )
  {
    v6 = 0;
    do
    {
      v7 = *(_QWORD *)(v5 + 8 * v6);
      if ( v7 != 0 )
      {
        if ( *a2 != nullptr && **a2 != 0 )
          sub_140809710(a2, 0x14193AE67LL, 0xFFFFFFFFLL);
        v16 = *(_BYTE *)(v7 + 48);
        sub_140808120(v17, &v16);
        v8 = *a2;
        if ( *a2 != nullptr && *v8 != 0 )
        {
          if ( v17[0] != 0 )
            v9 = *(unsigned int *)v17[0];
          else
            v9 = 0;
          v13 = v17[0] + 4LL;
          if ( v17[0] == 0 )
            v13 = 0x1419435F1LL;
          sub_140809710(a2, v13, v9);
        }
        else if ( v17 != a2 )
        {
          v10 = v8 - 1;
          if ( v8 == nullptr )
            v10 = nullptr;
          v11 = (volatile signed __int32 *)(v17[0] - 4LL);
          if ( v17[0] != 0 )
          {
            if ( v8 != nullptr && _InterlockedDecrement(v10) == 0 )
              sub_1412EC9A0((__int64)v10);
            *a2 = nullptr;
            _InterlockedIncrement(v11);
            v12 = v11 + 1;
          }
          else
          {
            if ( v8 != nullptr && _InterlockedDecrement(v10) == 0 )
              sub_1412EC9A0((__int64)v10);
            v12 = nullptr;
          }
          *a2 = v12;
        }
        v14 = v17[0];
        if ( v17[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v17[0] - 4LL)) == 0 )
          sub_1412EC9A0(v14 - 4);
        v4 = *(_QWORD *)(a1 + 24);
      }
      ++v6;
      v5 = *(_QWORD *)(v4 + 280);
    }
    while ( v6 < (*(_QWORD *)(v4 + 288) - v5) >> 3 );
  }
  return a2;
}
