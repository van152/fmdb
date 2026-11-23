// THUNK ALIAS -> sub_143E55330 (jmp:0x140ff5be0->0x143e55330)
char __fastcall sub_143E55330(__int64 a1, __int64 a2, __int64 *a3)
{
  __int64 v4; // rax
  __int64 *v5; // rsi
  __int64 v6; // rdx
  volatile signed __int32 *v7; // rcx
  volatile signed __int32 *v8; // rdi
  volatile signed __int32 *v9; // rdi

  v4 = sub_140FF4A70();
  if ( v4 != 0 )
  {
    v5 = (__int64 *)(v4 + 8);
    if ( (__int64 *)(v4 + 8) != a3 )
    {
      v6 = *a3;
      v4 = *v5;
      v7 = (volatile signed __int32 *)(*v5 - 4);
      if ( *v5 == 0 )
        v7 = nullptr;
      v8 = (volatile signed __int32 *)(v6 - 4);
      if ( v6 != 0 )
      {
        if ( v4 != 0 && _InterlockedDecrement(v7) == 0 )
          LOBYTE(v4) = sub_1412EC9A0((__int64)v7);
        *v5 = 0;
        _InterlockedIncrement(v8);
        v9 = v8 + 1;
      }
      else
      {
        if ( v4 != 0 && _InterlockedDecrement(v7) == 0 )
          LOBYTE(v4) = sub_1412EC9A0((__int64)v7);
        v9 = nullptr;
      }
      *v5 = (__int64)v9;
    }
  }
  return v4;
}
