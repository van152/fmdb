// THUNK ALIAS -> sub_144028540 (jmp:0x1411eaaa0->0x144028540)
char __fastcall sub_144028540(__int64 a1, __int64 a2, __int64 *a3)
{
  int v4; // ebx
  __int64 v5; // rsi
  char result; // al
  volatile signed __int32 **v7; // rsi
  volatile signed __int32 *v8; // rax
  volatile signed __int32 *v9; // rcx
  volatile signed __int32 *v10; // rdi
  volatile signed __int32 *v11; // rdi
  __int64 v12; // rcx
  _QWORD v13[4]; // [rsp+28h] [rbp-20h] BYREF

  v4 = a2;
  LOBYTE(a2) = 9;
  v5 = sub_1411EACB0(a1, a2, 0xFFFFFFFFLL, 0xFFFFFFFFLL);
  result = 0;
  if ( v4 > 1313302125 )
  {
    if ( v4 <= 1313304676 )
    {
      if ( v4 != 1313302126 )
      {
        if ( v4 != 1313302380 )
          return result;
        *(_WORD *)(v5 + 58) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
        return 1;
      }
      (*(void (__fastcall **)(__int64, _QWORD *, __int64 *))(*(_QWORD *)*a3 + 128LL))(*a3, v13, a3);
      v7 = (volatile signed __int32 **)(v5 + 40);
      if ( v7 == v13 )
        goto LABEL_35;
      goto LABEL_23;
    }
    if ( v4 == 1313305454 )
    {
      (*(void (__fastcall **)(__int64, _QWORD *, __int64 *))(*(_QWORD *)*a3 + 128LL))(*a3, v13, a3);
      v7 = (volatile signed __int32 **)(v5 + 48);
      if ( v7 == v13 )
      {
LABEL_35:
        v12 = v13[0];
        if ( v13[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v13[0] - 4LL)) == 0 )
          sub_1412EC9A0(v12 - 4);
        return 1;
      }
LABEL_23:
      v8 = *v7;
      v9 = *v7 - 1;
      if ( *v7 == nullptr )
        v9 = nullptr;
      v10 = (volatile signed __int32 *)(v13[0] - 4LL);
      if ( v13[0] != 0 )
      {
        if ( v8 != nullptr && _InterlockedDecrement(v9) == 0 )
          sub_1412EC9A0((__int64)v9);
        *v7 = nullptr;
        _InterlockedIncrement(v10);
        v11 = v10 + 1;
      }
      else
      {
        if ( v8 != nullptr && _InterlockedDecrement(v9) == 0 )
          sub_1412EC9A0((__int64)v9);
        v11 = nullptr;
      }
      *v7 = v11;
      goto LABEL_35;
    }
    if ( v4 != 1313304677 )
      return result;
    sub_140FE7960((__int64)v13, a3, 0);
    *(_QWORD *)(v5 + 16) = v13[0];
  }
  else
  {
    if ( v4 <= 1312911460 )
    {
      if ( v4 != 1312908910 )
      {
        if ( v4 != 1312909164 )
          return result;
        *(_WORD *)(v5 + 56) = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
        return 1;
      }
      (*(void (__fastcall **)(__int64, _QWORD *, __int64 *))(*(_QWORD *)*a3 + 128LL))(*a3, v13, a3);
      v7 = (volatile signed __int32 **)(v5 + 24);
      if ( v7 == v13 )
        goto LABEL_35;
      goto LABEL_23;
    }
    if ( v4 != 1312911461 )
    {
      if ( v4 != 1312912238 )
        return result;
      (*(void (__fastcall **)(__int64, _QWORD *, __int64 *))(*(_QWORD *)*a3 + 128LL))(*a3, v13, a3);
      v7 = (volatile signed __int32 **)(v5 + 32);
      if ( v7 == v13 )
        goto LABEL_35;
      goto LABEL_23;
    }
    sub_140FE7960((__int64)v13, a3, 0);
    *(_QWORD *)(v5 + 8) = v13[0];
  }
  return 1;
}
