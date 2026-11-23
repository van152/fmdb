bool __fastcall sub_14438F150(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rbx
  _BYTE v6[25]; // [rsp+2Fh] [rbp-19h] BYREF

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v6, a3: 1);
  return *(_DWORD *)(v4 + 16) == 0
      && (unsigned __int8)sub_14145C5A0(a1, a2) != 0
      && (unsigned __int8)sub_14145C700(a1: a1 + 24, a2) != 0
      && (unsigned __int8)sub_14145C700(a1: a1 + 56, a2) != 0
      && (unsigned __int8)sub_14145C700(a1: a1 + 88, a2) != 0
      && (unsigned __int8)sub_14145C700(a1: a1 + 120, a2) != 0
      && (unsigned __int8)sub_14145C700(a1: a1 + 152, a2) != 0
      && (unsigned __int8)sub_14145C700(a1: a1 + 184, a2) != 0
      && (unsigned __int8)sub_14145C700(a1: a1 + 216, a2) != 0
      && *(_DWORD *)(*a2 + 16LL) == 0;
}
