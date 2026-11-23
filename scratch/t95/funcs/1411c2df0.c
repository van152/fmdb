// THUNK ALIAS -> sub_144003C60 (jmp:0x1411c2df0->0x144003c60)
char __fastcall sub_144003C60(__int64 a1, __int64 a2, _QWORD *a3)
{
  char v5; // al
  volatile signed __int32 **v6; // rsi
  char result; // al
  __int64 v8; // rcx
  char v9; // cl
  volatile signed __int32 *v10; // rax
  volatile signed __int32 *v11; // rcx
  volatile signed __int32 *v12; // rdi
  volatile signed __int32 *v13; // rdi
  __int64 v14; // rcx
  _QWORD v15[4]; // [rsp+28h] [rbp-20h] BYREF

  if ( (int)a2 > 1131572083 )
  {
    if ( (int)a2 > 1416851040 )
    {
      if ( (_DWORD)a2 != 1416851041 )
      {
        if ( (_DWORD)a2 != 1416919408 )
          return sub_140FE2700(a1, a2, a3);
        *(_BYTE *)(a1 + 40) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
        return 1;
      }
      (*(void (__fastcall **)(_QWORD, _QWORD *, _QWORD *))(*(_QWORD *)*a3 + 128LL))(*a3, v15, a3);
      v6 = (volatile signed __int32 **)(a1 + 32);
      if ( v6 == v15 )
      {
LABEL_36:
        v14 = v15[0];
        if ( v15[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v15[0] - 4LL)) == 0 )
          sub_1412EC9A0(v14 - 4);
        return 1;
      }
    }
    else
    {
      if ( (_DWORD)a2 == 1131572084 )
      {
LABEL_14:
        result = 0;
        if ( *(_BYTE *)(a1 + 47) == 0 )
        {
          v8 = *(_QWORD *)(a1 + 48);
          if ( v8 != 0 )
            return sub_140E834A0(v8, a2, a3);
        }
        return result;
      }
      if ( (_DWORD)a2 != 1416392289 )
        return sub_140FE2700(a1, a2, a3);
      (*(void (__fastcall **)(_QWORD, _QWORD *, _QWORD *))(*(_QWORD *)*a3 + 128LL))(*a3, v15, a3);
      v6 = (volatile signed __int32 **)(a1 + 24);
      if ( v6 == v15 )
        goto LABEL_36;
    }
    v10 = *v6;
    v11 = *v6 - 1;
    if ( *v6 == nullptr )
      v11 = nullptr;
    v12 = (volatile signed __int32 *)(v15[0] - 4LL);
    if ( v15[0] != 0 )
    {
      if ( v10 != nullptr && _InterlockedDecrement(v11) == 0 )
        sub_1412EC9A0((__int64)v11);
      *v6 = nullptr;
      _InterlockedIncrement(v12);
      v13 = v12 + 1;
    }
    else
    {
      if ( v10 != nullptr && _InterlockedDecrement(v11) == 0 )
        sub_1412EC9A0((__int64)v11);
      v13 = nullptr;
    }
    *v6 = v13;
    goto LABEL_36;
  }
  if ( (int)a2 <= 1131307366 )
  {
    if ( (_DWORD)a2 != 1130586721 )
    {
      if ( (_DWORD)a2 == 1131241831 )
      {
        if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
          v5 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
        else
          v5 = -1;
        *(_BYTE *)(a1 + 44) = v5;
        result = 1;
        if ( *(_BYTE *)(a1 + 45) <= *(_BYTE *)(a1 + 44) )
          return result;
LABEL_45:
        if ( *(char *)(a1 + 44) > 0 )
          *(_BYTE *)(a1 + 45) = *(_BYTE *)(a1 + 44);
        return result;
      }
      return sub_140FE2700(a1, a2, a3);
    }
    goto LABEL_14;
  }
  if ( (_DWORD)a2 != 1131307367 )
  {
    if ( (_DWORD)a2 != 1131307380 )
      return sub_140FE2700(a1, a2, a3);
    goto LABEL_14;
  }
  if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 8LL))(*a3, a3) != 0 )
    v9 = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
  else
    v9 = -1;
  *(_BYTE *)(a1 + 45) = v9;
  result = 1;
  if ( v9 > *(char *)(a1 + 44) )
    goto LABEL_45;
  return result;
}
