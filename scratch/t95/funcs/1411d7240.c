// THUNK ALIAS -> sub_1440135B0 (jmp:0x1411d7240->0x1440135b0)
__int64 __fastcall sub_1440135B0(__int64 a1, char a2)
{
  unsigned int v2; // esi
  unsigned int v4; // eax
  int v5; // ecx
  int v6; // ebx
  __int64 v8; // rax

  if ( a2 != 0 || dword_141B60300 == 1000004 || dword_141B60300 == 8 )
  {
    LOBYTE(v2) = 1;
    v4 = *(_DWORD *)(a1 + 12) - 1478;
    if ( v4 > 0xB || (v5 = 2561, !_bittest(&v5, v4)) )
    {
      if ( *(_BYTE *)(a1 + 186) == 0
        && (((v6 = *(_DWORD *)(a1 + 352)) & 0x10800) != 0
         || (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)a1 + 416LL))(a1) != 0
         && *(_DWORD *)((*(__int64 (__fastcall **)(__int64))(*(_QWORD *)a1 + 416LL))(a1) + 12) == 788
         || (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)a1 + 416LL))(a1) == 0
         && (v8 = *(_QWORD *)(a1 + 224)) != 0
         && *(_DWORD *)(v8 + 12) == 788) )
      {
        LOBYTE(v2) = (v6 & 0x10800) != 0;
      }
    }
  }
  else
  {
    return 0;
  }
  return v2;
}
