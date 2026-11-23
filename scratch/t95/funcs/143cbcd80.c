char __fastcall sub_143CBCD80(__int64 a1, int a2, __int64 **a3)
{
  __int64 v5; // rax
  __int64 v6; // rdx
  volatile signed __int32 **v7; // rsi
  volatile signed __int32 *v8; // rax
  volatile signed __int32 *v9; // rcx
  volatile signed __int32 *v10; // rdi
  volatile signed __int32 *v11; // rdi
  __int64 v12; // rcx
  __int64 v13; // rax
  __int64 v14; // rax
  _QWORD v16[4]; // [rsp+28h] [rbp-20h] BYREF

  if ( a2 > 1130783853 )
  {
    if ( a2 > 1131443301 )
    {
      if ( a2 == 1131443302 )
      {
        v14 = sub_140FE35F0();
        if ( v14 != 0 )
          (*(void (__fastcall **)(__int64, __int64, __int64 **, _QWORD))(*(_QWORD *)qword_141B5EF38 + 216LL))(
            qword_141B5EF38,
            v14,
            a3,
            *(unsigned int *)(a1 + 12));
        return 1;
      }
      if ( a2 == 1131571059 )
      {
        *(float *)(a1 + 228) = (*(float (__fastcall **)(__int64 *, __int64 **))(**a3 + 96))(*a3, a3);
        return 1;
      }
      if ( a2 != 1131636334 )
        return sub_140FE2700((_DWORD *)a1, a2, a3);
      (*(void (__fastcall **)(__int64 *, _QWORD *, __int64 **))(**a3 + 128))(*a3, v16, a3);
      v7 = (volatile signed __int32 **)(a1 + 64);
      if ( v7 != v16 )
        goto LABEL_29;
    }
    else
    {
      switch ( a2 )
      {
        case 1130783854:
          (*(void (__fastcall **)(__int64 *, _QWORD *, __int64 **))(**a3 + 128))(*a3, v16, a3);
          v7 = (volatile signed __int32 **)(a1 + 48);
          if ( v7 != v16 )
            goto LABEL_29;
          break;
        case 1131307373:
          (*(void (__fastcall **)(__int64 *, _QWORD *, __int64 **))(**a3 + 128))(*a3, v16, a3);
          v7 = (volatile signed __int32 **)(a1 + 24);
          if ( v7 != v16 )
            goto LABEL_29;
          break;
        case 1131373414:
          v5 = sub_140FE35F0();
          if ( v5 != 0 )
            (*(void (__fastcall **)(__int64, __int64, __int64 **, _QWORD))(*(_QWORD *)qword_141B5EF38 + 184LL))(
              qword_141B5EF38,
              v5,
              a3,
              *(unsigned int *)(a1 + 12));
          return 1;
        default:
          return sub_140FE2700((_DWORD *)a1, a2, a3);
      }
    }
LABEL_41:
    v12 = v16[0];
    if ( v16[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v16[0] - 4LL)) == 0 )
      sub_1412EC9A0(v12 - 4, v6);
    return 1;
  }
  if ( a2 > 1129608290 )
  {
    if ( a2 == 1129608291 )
    {
      sub_140FE3B40(v16, a3);
      *(_DWORD *)(a1 + 80) = v16[0];
      return 1;
    }
    if ( a2 == 1130587756 )
    {
      v13 = sub_140FE35F0();
      if ( v13 != 0 )
        (*(void (__fastcall **)(__int64, __int64, __int64 **, _QWORD))(*(_QWORD *)qword_141B5EF38 + 168LL))(
          qword_141B5EF38,
          v13,
          a3,
          *(unsigned int *)(a1 + 12));
      return 1;
    }
    if ( a2 != 1130591353 )
      return sub_140FE2700((_DWORD *)a1, a2, a3);
    (*(void (__fastcall **)(__int64 *, _QWORD *, __int64 **))(**a3 + 128))(*a3, v16, a3);
    v7 = (volatile signed __int32 **)(a1 + 40);
    if ( v7 != v16 )
      goto LABEL_29;
    goto LABEL_41;
  }
  switch ( a2 )
  {
    case 1127443566:
      (*(void (__fastcall **)(__int64 *, _QWORD *, __int64 **))(**a3 + 128))(*a3, v16, a3);
      v7 = (volatile signed __int32 **)(a1 + 32);
      if ( v7 == v16 )
        goto LABEL_41;
LABEL_29:
      v6 = v16[0];
      v8 = *v7;
      v9 = *v7 - 1;
      if ( *v7 == nullptr )
        v9 = nullptr;
      v10 = (volatile signed __int32 *)(v16[0] - 4LL);
      if ( v16[0] != 0 )
      {
        if ( v8 != nullptr && _InterlockedDecrement(v9) == 0 )
          sub_1412EC9A0(v9, v6);
        *v7 = nullptr;
        _InterlockedIncrement(v10);
        v11 = v10 + 1;
      }
      else
      {
        if ( v8 != nullptr && _InterlockedDecrement(v9) == 0 )
          sub_1412EC9A0(v9, v6);
        v11 = nullptr;
      }
      *v7 = v11;
      goto LABEL_41;
    case 1129603683:
      sub_140FE3B40(v16, a3);
      *(_DWORD *)(a1 + 76) = v16[0];
      return 1;
    case 1129604707:
      sub_140FE3B40(v16, a3);
      *(_DWORD *)(a1 + 72) = v16[0];
      return 1;
    default:
      break;
  }
  return sub_140FE2700((_DWORD *)a1, a2, a3);
}
