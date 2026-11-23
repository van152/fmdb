char __fastcall sub_140E560C0(__int64 a1, __int64 a2, _QWORD *a3)
{
  __int64 v4; // rdx
  volatile signed __int32 **v5; // rsi
  volatile signed __int32 *v6; // rax
  volatile signed __int32 *v7; // rcx
  volatile signed __int32 *v8; // rdi
  volatile signed __int32 *v9; // rdi
  __int64 v10; // rdi
  __int64 *v11; // rcx
  __int64 v12; // rax
  __int64 v13; // rcx
  __int64 v14; // rdi
  __int64 v15; // rdi
  __int64 v16; // rdi
  __int64 *v17; // rcx
  __int64 v18; // rax
  __int64 v19; // rcx
  __int64 *v21; // rcx
  __int64 v22; // rax
  __int64 v23; // rcx
  __int64 v24; // rcx
  _QWORD v25[4]; // [rsp+28h] [rbp-20h] BYREF

  if ( (int)a2 <= 1131179885 )
  {
    if ( (int)a2 <= 1130983015 )
    {
      if ( (_DWORD)a2 == 1130458228 )
      {
        *(_WORD *)(a1 + 80) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      }
      else
      {
        if ( (_DWORD)a2 != 1130460276 )
          return sub_140FE2700(a1, a2, a3);
        *(_BYTE *)(a1 + 84) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
      }
    }
    else
    {
      switch ( (_DWORD)a2 )
      {
        case 0x43696E68:
          *(_BYTE *)(a1 + 82) = (*(__int64 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 64LL))(*a3, a3);
          break;
        case 0x436C6174:
          *(float *)(a1 + 72) = (*(float (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 96LL))(*a3, a3);
          break;
        case 0x436C6769:
          v10 = qword_141B5FDF8;
          sub_140FE7960(v25, a3, 1818324583);
          *(_QWORD *)(a1 + 48) = sub_140FA1860(v10, v25);
          break;
        default:
          return sub_140FE2700(a1, a2, a3);
      }
    }
  }
  else if ( (int)a2 > 1131312232 )
  {
    switch ( (_DWORD)a2 )
    {
      case 0x436E7469:
        v15 = qword_141B5FDD0;
        sub_140FE7960(v25, a3, 1315856756);
        *(_QWORD *)(a1 + 32) = sub_14002F670(v15, v25);
        break;
      case 0x43776561:
        v16 = qword_141B5FE48;
        sub_140FE7960(v25, a3, 2004117618);
        *(_QWORD *)(a1 + 40) = sub_140FA1860(v16, v25);
        break;
      case 0x44454C45:
        v11 = *(__int64 **)(qword_141B5FE28 + 128);
        v12 = *v11;
        v13 = v11[1];
        while ( v12 != v13 )
        {
          if ( *(_QWORD *)(*(_QWORD *)v12 + 80LL) == a1 )
            *(_QWORD *)(*(_QWORD *)v12 + 80LL) = 0;
          v12 += 8;
        }
        v17 = *(__int64 **)(qword_141B5FDF0 + 128);
        v18 = *v17;
        v19 = v17[1];
        while ( v18 != v19 )
        {
          if ( *(_QWORD *)(*(_QWORD *)v18 + 192LL) == a1 )
            *(_QWORD *)(*(_QWORD *)v18 + 192LL) = 0;
          v18 += 8;
        }
        v21 = *(__int64 **)(qword_141B5FDD0 + 128);
        v22 = *v21;
        v23 = v21[1];
        while ( v22 != v23 )
        {
          if ( *(_QWORD *)(*(_QWORD *)v22 + 232LL) == a1 )
            *(_QWORD *)(*(_QWORD *)v22 + 232LL) = 0;
          v22 += 8;
        }
        *(_BYTE *)(a1 + 85) |= 1u;
        return 1;
      default:
        return sub_140FE2700(a1, a2, a3);
    }
  }
  else
  {
    switch ( (_DWORD)a2 )
    {
      case 0x436C6F6E:
        *(float *)(a1 + 76) = (*(float (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 96LL))(*a3, a3);
        break;
      case 0x436C7269:
        v14 = qword_141B5FE00;
        sub_140FE7960(v25, a3, 1818456679);
        *(_QWORD *)(a1 + 56) = sub_140FA1860(v14, v25);
        break;
      case 0x436E616D:
        (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*a3 + 128LL))(*a3, v25);
        v5 = (volatile signed __int32 **)(a1 + 24);
        if ( v5 != v25 )
        {
          v4 = v25[0];
          v6 = *v5;
          v7 = *v5 - 1;
          if ( *v5 == nullptr )
            v7 = nullptr;
          v8 = (volatile signed __int32 *)(v25[0] - 4LL);
          if ( v25[0] != 0 )
          {
            if ( v6 != nullptr && _InterlockedDecrement(v7) == 0 )
              sub_1412EC9A0(v7, v4);
            *v5 = nullptr;
            _InterlockedIncrement(v8);
            v9 = v8 + 1;
          }
          else
          {
            if ( v6 != nullptr && _InterlockedDecrement(v7) == 0 )
              sub_1412EC9A0(v7, v4);
            v9 = nullptr;
          }
          *v5 = v9;
        }
        v24 = v25[0];
        if ( v25[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v25[0] - 4LL)) == 0 )
          sub_1412EC9A0(v24 - 4, v4);
        return 1;
      default:
        return sub_140FE2700(a1, a2, a3);
    }
  }
  return 1;
}
